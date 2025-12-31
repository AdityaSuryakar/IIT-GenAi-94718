from about_us import scrape_sunbeam_about_us
from apache import scrape_apache_details
from aptitude import scrape_aptitude_course
from available_internship import available_internship
from cpp import scrape_cpp_course
from dev_ops import scrape_dev_ops
from dream_llm import scrape_dream_llm
from dsa import scrape_dsa
from genai import  scrape_genai
from intenship_details import internship_details
from java import scrape_java
from mern import scrape_mern
from ml import ml
from mlops_llmops import llmops_mlops
from pre_cat import precat
from python_dev import python_dev

scraper_funtion =[
    scrape_sunbeam_about_us,
    scrape_apache_details,
    scrape_aptitude_course,
    available_internship,
    scrape_cpp_course,
    scrape_dev_ops,
    scrape_dream_llm,
    scrape_dsa,
    scrape_genai,
    internship_details,
    scrape_java,
    scrape_mern,
    ml,
    llmops_mlops,
    precat,
    python_dev
]

def run_all_scraperrs():
    all_data=[]
    for scraper in scraper_funtion:
        try:
            data = scraper()
            if data:
                all_data.append(data)
        except Exception as e:
            print(f"Error in {scraper.__name__}: {e}")
           
    return all_data
    


# import chromadb

# client = chromadb.PersistentClient(path="chroma_db_no_split")
# col = client.get_collection("sunbeam_data")

# data = col.get(include=["documents", "metadatas", "embeddings"])

# print("Total records:", len(data["ids"]))

# for i in range(len(data["ids"])):
#     print("\nID:", data["ids"][i])
#     print("Document:", data["documents"][i])
#     print("Metadata:", data["metadatas"][i])
#     print("Embedding length:", len(data["embeddings"][i]))