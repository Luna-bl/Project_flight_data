import streamlit as st

st.title("Flight Data Explorer — Report")

st.markdown("""
## Dataset

- Samples: 1500  
- Approx sampling rate: 1.00 Hz  

## Metrics

- **climb_gradient_m_per_m**: 0.0861774793809889  
- **tas_stability_std_mps_over_60s**: 1.2452437663861147  
- **descent_energy_rate_m2_per_s3**: -47.34374821651866  
""")

st.image('docs/figures/altitude_profile.png', width=700)
st.image('docs/figures/vertical_speed.png', width=700)
st.image('docs/figures/plan_view.png', width=700)
st.image('docs/figures/speed_phase_timeline.png', width=700)
