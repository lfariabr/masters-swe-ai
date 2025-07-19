# pages/TopicModeling.py

import streamlit as st
import pandas as pd
from resolvers.BERTopicModel import train_bertopic_model
from utils.preprocessing import classify_nps, calculate_nps

st.title("🔍 Topic Modeling (BERTopic)")

def show_topic_modeling():
    uploaded_file = st.file_uploader("Upload your CSV", type="csv")

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
                    # 1. Filtrar comentários válidos
                    valid_mask = df["Comment"].notna() & df["Comment"].str.strip().ne("")
                    valid_comments = df.loc[valid_mask, "Comment"]

                    # 2. Treinar modelo
                    model, topics, probs, embeddings = train_bertopic_model(valid_comments)

                    # 3. Atribuir tópicos às linhas válidas
                    df.loc[valid_mask, "Topic"] = topics
                    df_topics = model.get_topic_info()
                    df_topics["Name"] = df_topics.apply(
                        lambda row: "Outliers" if row["Topic"] == -1 else row["Name"], axis=1
                    )

                    # 4. Adicionar nomes dos tópicos ao df
                    df = df.merge(df_topics[["Topic", "Name"]], on="Topic", how="left")

                    st.success("BERTopic modeling complete!")

                    # Show basic topic info
                    st.write("### Top Topics")
                    st.dataframe(df_topics.head(10))

                    # Plot topics
                    st.plotly_chart(model.visualize_barchart(top_n_topics=5))

                    # 5. Calcular NPS por tópico
                    topic_nps_df = (
                        df[df["Topic"] != -1]  # Ignorar outliers
                        .groupby("Name")
                        .agg(
                            Count=("Comment", "count"),
                            Avg_Score=("Score", "mean"),
                            NPS_Score=("NPS Type", lambda x: calculate_nps(pd.DataFrame({"NPS Type": x})))
                        )
                        .reset_index()
                        .sort_values(by="Count", ascending=False)
                    )

                    st.write("### 🧠 Topic-wise NPS Stats")
                    st.dataframe(topic_nps_df)