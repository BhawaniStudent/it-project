import streamlit as st

st.title("Digital Forensics Log Analyzer")

if "logs" not in st.session_state:
    st.session_state.logs = []

log = st.text_input("Enter log")

if st.button("Add Log"):
    if log:
        st.session_state.logs.append(log)

st.subheader("Logs")
for l in st.session_state.logs:
    st.write(l)

if st.button("Analyze Logs"):
    total = len(st.session_state.logs)
    suspicious = [l for l in st.session_state.logs if "error" in l.lower() or "failed" in l.lower()]

    st.write("Total Logs:", total)
    st.write("Suspicious Logs:", len(suspicious))
