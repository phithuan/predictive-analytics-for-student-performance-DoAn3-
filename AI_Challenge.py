import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="HORUS: Video Retrieval", layout="wide")
st.title("🎥 HORUS: Video Retrieval 🎥")

# Sidebar: Truy vấn
st.sidebar.header("Query")
query_id = st.sidebar.text_input("Query ID")
query_text = st.sidebar.text_area("Query", "The school of fish swims around the coral.")

use_query_expansion = st.sidebar.radio("Use Query Expansion", ["True", "False"], index=0)
clip_weight = st.sidebar.slider("CLIP Weight", 0.0, 1.0, 0.5, 0.05)
caption_weight = st.sidebar.slider("Caption Weight", 0.0, 1.0, 0.5, 0.05)
top_k = st.sidebar.slider("Top-K", 1, 100, 20)

# Nút truy vấn
if st.sidebar.button("Query"):
    st.session_state["submitted"] = True
    st.session_state["query_result"] = f"Querying top {top_k} results with CLIP: {clip_weight}, Caption: {caption_weight}"

# Kết quả truy vấn
st.subheader("🔎 Search Results")
if st.session_state.get("submitted"):
    st.success(st.session_state["query_result"])
    # Placeholder for video keyframe grid or preview
    st.info("[Placeholder] Displaying top-K retrieved keyframes/videos")

# Dump file (giống nút download)
st.subheader("📥 Dump")
st.download_button("Download Submission File", data="submission_content", file_name="submission.txt")

# Khu vực rerank
col1, col2 = st.columns(2)
with col1:
    st.button("Rerank One")
with col2:
    st.button("Rerank All")
