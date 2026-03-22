import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import io
from collections import defaultdict

from network import (ROUTES, STOP_ROUTES, HUB_STOPS,
                     SOURCE, DESTINATION, TRANSFER_COST)
from environment import reset_episode, make_fixed_env
from mdp import get_state, get_valid_actions, get_reward
from agent import train, get_best_path, export_qtable_csv
from visualize import plot_learning_curve, plot_network, plot_qtable

# ── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title='Transport Route Optimizer',
    layout='wide',
    page_icon='🚌'
)

# ── HEADER ───────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1F4E79;padding:1.1rem 1.5rem;
            border-radius:8px;margin-bottom:1.4rem;">
  <h2 style="color:white;margin:0;font-size:1.5rem;">
    🚌 Public Transport Route Optimizer
  </h2>
  <p style="color:#BFD7ED;margin:0.3rem 0 0;font-size:0.92rem;">
    Q-Learning &nbsp;|&nbsp; 25 stops &nbsp;·&nbsp;
    8 Bus &nbsp;·&nbsp; 5 Metro &nbsp;·&nbsp; 12 Auto &nbsp;|&nbsp;
    Time = length ÷ (speed ÷ congestion) × 60
  </p>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────
for key, default in {
    'Q':               None,
    'rewards':         None,
    'best_path':       None,
    'best_path_stops': None,
    'total_time':      None,
    'total_dist':      None,
    'training_done':   False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.title('⚙️ Configuration')

    st.subheader('Network Settings')
    source = st.selectbox(
        'Source Stop', list(range(25)),
        format_func=lambda x: f'S{x}', index=0)
    destination = st.selectbox(
        'Destination Stop', list(range(25)),
        format_func=lambda x: f'S{x}', index=24)

    if source == destination:
        st.error('Source and destination must be different.')

    st.divider()
    st.subheader('Hyperparameters')
    episodes     = st.slider('Episodes',           500,  5000, 2000, 100)
    alpha        = st.slider('Learning rate (α)',  0.01, 0.50, 0.10, 0.01)
    gamma        = st.slider('Discount (γ)',       0.50, 1.00, 0.90, 0.01)
    epsilon_init = st.slider('Initial ε',          0.50, 1.00, 1.00, 0.05)

    st.divider()
    st.subheader('Environment')
    time_band_radio = st.radio(
        'Time Band',
        ['Random each episode', 'Always peak', 'Always off-peak'])
    closure_prob = st.slider(
        'Route closure probability', 0.00, 0.30, 0.10, 0.01)

    st.divider()

    # Single combined button
    run_btn   = st.button(
        '▶  Run & Find Optimal Path',
        type='primary',
        use_container_width=True,
        disabled=(source == destination)
    )
    reset_btn = st.button(
        '🔄  Reset',
        use_container_width=True)

    # Q-table download — shown only after training
    if st.session_state.training_done and st.session_state.Q:
        st.divider()
        st.subheader('Export')
        Q_loaded = defaultdict(float, st.session_state.Q)
        qt_rows  = export_qtable_csv(Q_loaded)
        buf = io.StringIO()
        if qt_rows:
            writer = csv.DictWriter(buf, fieldnames=qt_rows[0].keys())
            writer.writeheader()
            writer.writerows(qt_rows)
        st.download_button(
            label='⬇  Download Q-Table (CSV)',
            data=buf.getvalue().encode('utf-8'),
            file_name='qtable_export.csv',
            mime='text/csv',
            use_container_width=True,
        )
        st.caption(f'{len(qt_rows)} entries · sorted by Q-value ↓')

    if st.session_state.training_done:
        st.success('Training complete ✓')

# ── TIME BAND MAP ────────────────────────────────────────────────
tb_map = {
    'Random each episode': 'random',
    'Always peak':         'peak',
    'Always off-peak':     'off_peak',
}
time_band_setting = tb_map[time_band_radio]

# ── BUTTON HANDLER ───────────────────────────────────────────────
if run_btn and source != destination:

    # Step 1 — Training
    prog_bar = st.progress(0, text='Initialising training...')
    status   = st.empty()

    def cb(ep, total, rews):
        pct = ep / total
        avg = np.mean(rews[-50:]) if len(rews) >= 50 else np.mean(rews)
        prog_bar.progress(
            pct, text=f'Training — episode {ep}/{total}  |  '
                       f'avg reward: {avg:.1f}')
        eps_now = max(0.01, epsilon_init * (0.995 ** ep))
        status.caption(f'Exploration ε = {eps_now:.4f}')

    Q, rewards = train(
        episodes=episodes,
        alpha=alpha,
        gamma=gamma,
        epsilon_start=epsilon_init,
        time_band_setting=time_band_setting,
        closure_prob=closure_prob,
        source=source,
        destination=destination,
        progress_callback=cb,
    )

    prog_bar.progress(1.0, text='Extracting optimal path...')
    status.caption('')

    # Step 2 — Path extraction (immediately after training)
    Q_dd  = defaultdict(float, Q)
    path, total_time, total_dist = get_best_path(Q_dd, source, destination)

    # Step 3 — Store everything
    st.session_state.Q               = dict(Q)
    st.session_state.rewards         = rewards
    st.session_state.best_path       = path
    st.session_state.best_path_stops = [p['stop'] for p in path]
    st.session_state.total_time      = total_time
    st.session_state.total_dist      = total_dist
    st.session_state.training_done   = True

    prog_bar.empty()
    status.empty()
    st.rerun()

if reset_btn:
    for key in ['Q', 'rewards', 'best_path', 'best_path_stops',
                'total_time', 'total_dist', 'training_done']:
        st.session_state[key] = None
    st.session_state.training_done = False
    st.rerun()

# ── MAIN PAGE CONTENT (shown only after training) ────────────────
if not st.session_state.training_done:
    st.info(
        '👈 Set your parameters in the sidebar and click '
        '"▶ Run & Find Optimal Path" to begin.'
    )
    st.stop()

# ────────────────────────────────────────────────────────────────
# SECTION 1 — SUMMARY METRICS
# ────────────────────────────────────────────────────────────────
rewards    = st.session_state.rewards
best_path  = st.session_state.best_path
total_time = st.session_state.total_time
total_dist = st.session_state.total_dist

reached = (best_path[-1]['stop'] == destination
           if best_path else False)

st.subheader('📊 Training Summary')
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric('Episodes Trained',     f'{len(rewards)}')
m2.metric('Final Avg Reward',     f'{np.mean(rewards[-100:]):.1f}')
m3.metric('Journey Time',         f'{total_time} min'
                                   if reached else 'Path incomplete')
m4.metric('Journey Distance',     f'{total_dist} km'
                                   if reached else '—')
m5.metric('Destination Reached',  '✅ Yes' if reached else '❌ No')

st.divider()

# ────────────────────────────────────────────────────────────────
# SECTION 2 — NETWORK MAP  (full width)
# ────────────────────────────────────────────────────────────────
st.subheader('🗺️ Network Map')
fig_net = plot_network(
    st.session_state.best_path_stops, source, destination)
st.pyplot(fig_net, use_container_width=True)
plt.close(fig_net)
st.caption(
    '🔵 Blue = Bus  |  🟢 Green = Metro  |  🟠 Amber = Auto  |  '
    '🔴 Red = Learned optimal path  |  🟣 Purple = Transfer hub'
)

st.divider()

# ────────────────────────────────────────────────────────────────
# SECTION 3 — LEARNING CURVE + Q-TABLE  (side by side)
# ────────────────────────────────────────────────────────────────
st.subheader('📈 Learning Curve  &  🔥 Q-Table')
col_lc, col_qt = st.columns(2)

with col_lc:
    fig_lc = plot_learning_curve(rewards)
    st.pyplot(fig_lc, use_container_width=True)
    plt.close(fig_lc)

    w      = min(50, max(1, len(rewards) // 10))
    smooth = np.convolve(rewards, np.ones(w) / w, mode='valid')
    best_ep = int(np.argmax(smooth)) + w if len(smooth) > 0 else 0
    st.caption(
        f'Best moving avg: {float(np.max(smooth)):.1f}  |  '
        f'Convergence episode: {best_ep}'
    )

with col_qt:
    Q_loaded = defaultdict(float, st.session_state.Q)
    fig_qt   = plot_qtable(Q_loaded)
    st.pyplot(fig_qt, use_container_width=True)
    plt.close(fig_qt)
    st.caption(
        'Green = positive future value learned.  '
        'Red = stop rarely visited or frequently blocked.'
    )

st.divider()

# ────────────────────────────────────────────────────────────────
# SECTION 4 — OPTIMAL PATH TABLE  (full width)
# ────────────────────────────────────────────────────────────────
st.subheader('🏁 Optimal Path — S{} → S{}'.format(source, destination))

if not reached:
    st.warning(
        'The agent did not reach the destination. '
        'Try increasing Episodes to 3000 or 4000, or increase '
        'the destination bonus in mdp.py from 200 to 300.'
    )

if best_path:
    rows = []
    cumulative = 0.0
    for i, step in enumerate(best_path):
        cumulative += step['time']
        rows.append({
            'Step':          i,
            'Stop':          f"S{step['stop']}",
            'Route':         step['route'],
            'Action':        step['action'],
            'Step time':     f"+{step['time']} min",
            'Cumulative':    f"{round(cumulative, 1)} min",
            'Distance (km)': step['distance_km'],
            'Speed (km/h)':  step['speed_kmh'],
        })

    df = pd.DataFrame(rows)

    # Colour-code rows by action type using pandas Styler
    def colour_row(row):
        if row['Action'] == 'start':
            return ['background-color: #1a3a52; color: white'] * len(row)
        elif row['Action'] == 'transfer':
            return ['background-color: #3b2270; color: white'] * len(row)
        elif row['Stop'] == f'S{destination}':
            return ['background-color: #14532d; color: white'] * len(row)
        else:
            return [''] * len(row)

    styled = df.style.apply(colour_row, axis=1)
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.caption(
        '🟦 Blue row = journey start  |  '
        '🟣 Purple row = mode transfer  |  '
        '🟢 Green row = destination reached'
    )
