import streamlit as st
import os
from engine.parser import extract_content
from engine.analyzer import analyze_skills
from engine.grammar import check_grammar
from engine.reporter import generate_pdf_report
from engine.experience import calculate_experience

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="PrepMate | ATS Simulator", layout="wide", initial_sidebar_state="expanded")

st.title("🚀 PrepMate: Industry Standard ATS Matcher")
st.markdown("Analyze your resume strictly against the specific job description requirements.")
st.markdown("---")

# 2. UI LAYOUT: INPUT SECTION
col1, col2 = st.columns(2)

with col1:
    st.header("📄 1. Upload Resume")
    uploaded_file = st.file_uploader("Upload your PDF or DOCX file", type=['pdf', 'docx'])
    
    role = st.selectbox("🎯 Target Role", [
        "Backend_Developer", "Frontend_Developer", "Fullstack_Developer", 
        "DevOps_Engineer", "Data_Scientist", "Mobile_Developer", 
        "QA_Engineer", "Cyber_Security", "AI_Engineer", "Data_Engineer"
    ])

with col2:
    st.header("💼 2. Job Description")
    jd_text = st.text_area("Paste the exact Job Description here...", height=200)

# 3. ANALYSIS EXECUTION
if st.button("Analyze Application", type="primary", use_container_width=True):
    if uploaded_file and jd_text:
        with st.spinner('🔄 Parsing resume and comparing against job requirements...'):
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # PHASE 1: Extraction & Logic (JD-First)
                raw_text = extract_content(temp_path)
                
                # The engine now takes the JD text to filter required skills!
                skill_results = analyze_skills(raw_text, jd_text, role)
                jd_score = skill_results['score']
                
                grammar_errors = check_grammar(raw_text)
                years_exp = calculate_experience(raw_text)
                
                # PHASE 2: Display Results
                st.success("✅ ATS Scan Complete!")
                st.divider()
                
                # --- Executive Dashboard ---
                st.markdown("### 📊 Executive Summary")
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    st.metric(label="JD Match Score", value=f"{jd_score}%", delta="Suitability")
                with col_m2:
                    st.metric(label="Calculated Experience", value=f"{years_exp}+ Years", delta="Extracted")
                with col_m3:
                    st.metric(label="Grammar Issues", value=len(grammar_errors), delta="To Fix", delta_color="inverse")

                st.progress(jd_score / 100)
                st.divider()

                # --- Deep Skill Analysis (Tabs) ---
                st.markdown("### 🛠️ Required Skills Breakdown")
                st.caption("Showing ONLY the skills requested in the Job Description.")
                
                categories = list(skill_results.get('detailed', {}).keys())
                if categories:
                    tabs = st.tabs(categories)
                    
                    for i, tab in enumerate(tabs):
                        category_name = categories[i]
                        cat_data = skill_results['detailed'][category_name]
                        
                        with tab:
                            col_f, col_m = st.columns(2)
                            with col_f:
                                st.markdown("#### ✅ Matched Requirements")
                                if cat_data['found']:
                                    for skill in cat_data['found']:
                                        st.success(skill)
                                else:
                                    st.write("None matched in this category.")
                                    
                            with col_m:
                                st.markdown("#### 🚩 Missing Requirements")
                                if cat_data['missing']:
                                    for skill in cat_data['missing']:
                                        st.error(skill)
                                else:
                                    st.info("Perfect! No missing skills here.")
                else:
                    st.warning("No skills from our database were detected in this Job Description.")

                st.divider()
                
                # --- Professionalism & Grammar ---
                st.markdown("### ✍️ Professionalism Check")
                if grammar_errors:
                    for err in grammar_errors:
                        with st.expander(f"Issue: {err['message']}"):
                            st.write(f"**Context:** ...{err['context']}...")
                            st.markdown(f"**💡 Suggestion:** Change to `<span style='color:green;font-weight:bold'>{err['suggestion']}</span>`", unsafe_allow_html=True)
                else:
                    st.success("No major grammatical issues found. Clean resume!")

                # PHASE 3: Report Generation
                st.divider()
                st.subheader("📥 4. Download Report")
                
                # Because the score in skill_results is now accurate, the PDF will be accurate.
                report_data = generate_pdf_report(skill_results, role, grammar_errors,jd_score)
                
                st.download_button(
                    label="Download ATS Analysis Report (PDF)",
                    data=report_data,
                    file_name=f"PrepMate_{role}_ATS_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    else:
        st.warning("Please upload a resume file and paste a Job Description first.")