# pip install streamlit
import streamlit as st



def main():
    st.title("Streamlit ECharts Demo")

    with st.sidebar:
        st.header("Configuration")
        api_options = ("echarts", "pyecharts")
        selected_api = st.selectbox(
            label="Choose your preferred API:",
            options=api_options,
        )


        if selected_api == "echarts":
            st.caption(
                """ECharts demos are extracted from https://echarts.apache.org/examples/en/index.html, 
            by copying/formattting the 'option' json object into st_echarts.
            Definitely check the echarts example page, convert the JSON specs to Python Dicts and you should get a nice viz."""
            )
        if selected_api == "pyecharts":
            st.caption(
                """Pyecharts demos are extracted from https://github.com/pyecharts/pyecharts-gallery,
            by copying the pyecharts object into st_pyecharts. 
            Pyecharts is still using ECharts 4 underneath, which is why the theming between st_echarts and st_pyecharts is different."""
            )

        if st.button("Generate raw clips"):
            print("generate raw clips")
    
        if st.button("Resize and mix videos"):
            print("Resize and mix videos")
    
        if st.button("Upload to youtube"):
            print("Upload to youtube")

        if st.button("Upload to facebook"):
            print("Upload to facebook")


    with st.expander("Source Code"):
        st.code("test code....")
    st.markdown(f"Credit: url")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Streamlit ECharts Demo", page_icon=":chart_with_upwards_trend:"
    )
    main()
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by @NR</h6>',
            unsafe_allow_html=True,
        )
