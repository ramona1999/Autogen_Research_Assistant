import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

load_dotenv()

print("ok")

st.title("Visual Research Assistant")

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("Gorq API Key is not set. Please set in the environment variables.")
    st.stop()

agents = ResearchAgents(groq_api_key)

data_loader = DataLoader()

query = st.text_input("Enter a Research topic:")

if st.button("Search"):
    with st.spinner("Fetching research papers..."):  # Show a loading spinner
        
        # Fetch research papers from ArXiv and Google Scholar
        arxiv_papers = data_loader.fetch_arxiv_papers(query)
        google_scholar_papers = data_loader.fetch_google_scholar_papers(query)
        all_papers = arxiv_papers + google_scholar_papers  # Combine results from both sources
        all_papers = google_scholar_papers

        # If no papers are found, display an error message
        if not all_papers:
            st.error("Failed to fetch papers. Try again!")
        else:
            processed_papers = []

            # Process each paper: generate summary and analyze advantages/disadvantages
            for paper in all_papers:
                summary = agents.summarize_paper(paper['summary'])  # Generate summary
                adv_dis = agents.analyze_advantages_disadvantages(summary)  # Analyze pros/cons

                processed_papers.append({
                    "title": paper["title"],
                    "link": paper["link"],
                    "summary": summary,
                    "advantages_disadvantages": adv_dis,
                })

            # Display the processed research papers
            st.subheader("Top Research Papers:")
            for i, paper in enumerate(processed_papers, 1):
                st.markdown(f"### {i}. {paper['title']}")  # Paper title
                st.markdown(f"🔗 [Read Paper]({paper['link']})")  # Paper link
                st.write(f"**Summary:** {paper['summary']}")  # Paper summary
                st.write(f"{paper['advantages_disadvantages']}")  # Pros/cons analysis
                st.markdown("---")  # Separator between papers