# pages/TopicModeling.py

import streamlit as st
import pandas as pd
from resolvers.BERTopicModel import train_bertopic_model
from utils.preprocessing import classify_nps, calculate_nps
from utils.data_upload import data_upload

def show_topic_modeling():
    """
    Main function for the Models Comparison Page.
    Implements enterprise-grade ML model comparison interface.
    """
    st.title("💥 Topic Modeling (BERTopic)")
    st.markdown("""
    Experiments with Training.
    """)

    data_upload()
    
    uploaded_file = st.file_uploader(
        "Upload your CSV file with customer feedback or use the sample data",
        type="csv",
        help="File should contain 'Comment' and 'Score' columns"
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df = classify_nps(df)
        
        if 'Comment' not in df.columns:
            st.error("Column 'Comment' not found in the uploaded file.")
        else:
            with st.expander("👀 Data Preview (just in case you want to check it)"):
                st.dataframe(df.sample(min(5, len(df))), use_container_width=True)
                st.info(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            if st.button("Run BERTopic"):
                with st.spinner("Training BERTopic model..."):
                    # 1. Filter valid comments
                    valid_mask = df["Comment"].notna() & df["Comment"].str.strip().ne("")
                    valid_comments = df.loc[valid_mask, "Comment"]

                    # 2. Train BERTopic model
                    model, topics, probs, embeddings = train_bertopic_model(valid_comments)

                    # 3. Assign topics to valid rows
                    df.loc[valid_mask, "Topic"] = topics
                    df_topics = model.get_topic_info()
                    df_topics["Name"] = df_topics.apply(
                        lambda row: "Outliers" if row["Topic"] == -1 else row["Name"], axis=1
                    )

                    # 4. Add topic names to df
                    df = df.merge(df_topics[["Topic", "Name"]], on="Topic", how="left")

                    st.success("BERTopic modeling complete!")

                    # Show basic topic info
                    st.write("---")
                    st.write("### Top Topics")
                    st.dataframe(df_topics.head(10))
                    st.write("---")

                    # Plot topics
                    st.plotly_chart(model.visualize_barchart(top_n_topics=5))
                    st.write("---")

                    # 5. Calculate NPS per topic
                    topic_nps_df = (
                        df[df["Topic"] != -1]  # Ignore outliers
                        .groupby("Name")
                        .agg(
                            Count=("Comment", "count"),
                            # Avg_Score=("Score", "mean"),
                            NPS_Score=("NPS Type", lambda x: calculate_nps(pd.DataFrame({"NPS Type": x})))
                        )
                        .reset_index()
                        .sort_values(by="Count", ascending=False)
                    )

                    st.write("### Topic-wise NPS Stats")
                    st.dataframe(topic_nps_df)
                    st.write("---")
    else:
        st.info("""
        👆 **Upload a CSV file to begin topic modeling**
        
        Your file should contain:
        - `Comment` column: Customer feedback text
        - `Score` column: Numerical rating (0-10)
        - Optional: `Date`, `Store` columns for additional analysis
        """)