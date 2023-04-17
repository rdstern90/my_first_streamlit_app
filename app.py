import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
import nltk
nltk.download('stopwords')
nltk.download('punkt')


# Function to read text file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# Function to generate bar chart
def generate_bar_chart(text, remove_stop_words=True, min_word_count=40):
    # Remove punctuation and convert to lowercase
    text = ''.join([char for char in text if char.isalpha() or char.isspace()]).lower()
    # Split text into words
    words = text.split()
    # Remove stop words if requested
    if remove_stop_words:
        stopwords = set(STOPWORDS)
        words = [word for word in words if word not in stopwords]
    # Count the occurrence of each word
    word_count = Counter(words)
    # Get the top X most frequent words
    top_words = dict(word_count.most_common(min_word_count))
    # Create horizontal bar chart
    fig, ax = plt.subplots()
    sorted_word_count = sorted(top_words.items(), key=lambda x: x[1], reverse=False)
    ax.barh([word for word, count in sorted_word_count], [count for word, count in sorted_word_count])
    for i, (word, count) in enumerate(sorted_word_count):
        ax.text(count + 1, i, count, ha='left', va='center')
    ax.set_title('Word Count')
    ax.set_xlabel('Count')
    ax.set_ylabel('Word')
    return fig

# Function to generate word cloud
def generate_word_cloud(text, remove_stop_words=True, max_words=100, size_largest_word=100, image_width=450, random_state=50):
    # Remove punctuation and convert to lowercase
    text = ''.join([char for char in text if char.isalpha() or char.isspace()]).lower()
    # Split text into words
    words = text.split()

    # define empty list of stopwords
    stopwords = []
    # only populate the stopword list if box is checked
    if remove_stop_words:
        stopwords = set(nltk.corpus.stopwords.words('english'))
        stopwords.update(['us', 'one', 'though','will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came','thou'])

    wc = WordCloud(background_color = "white", 
                        max_words = max_words, 
                        max_font_size=size_largest_word, 
                        stopwords = stopwords, 
                        random_state=random_state,
                        width=image_width)

    wc.generate_from_text(' '.join(words))

    # Plot word cloud
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')

    return fig

# Set up sidebar
st.sidebar.title('Word Cloud Settings')
max_words = st.sidebar.slider('Max Words', min_value=10, max_value=200, value=100, step=10)
size_largest_word = st.sidebar.slider('Size of Largest Word', min_value=50, max_value=350, value=60, step=10)
image_width = st.sidebar.slider('Image Width', min_value=100, max_value=800, value=400, step=10)
random_state = st.sidebar.slider('Random State', min_value=20, max_value=100, value=20, step=1)
remove_stop_words = st.sidebar.checkbox('Remove Stop Words', value=True)
min_word_count = st.sidebar.slider('Minimum Count of Words', min_value=1, max_value=100, value=40, step=1)

# Set up main content area

# Create a dictionary (not a list)
books = {"":"","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}

st.markdown('''
# Analyzing Shakespeare Texts
''')
book_selected = st.selectbox('Choose a text file:', books.keys())

## Get the filename
file_selected = books.get(book_selected)


if file_selected != "":
    text = read_file(file_selected)
    # Create tabs
    word_cloud_tab, bar_chart_tab, view_text_tab = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

    with word_cloud_tab:
        # Generate word cloud
        fig = generate_word_cloud(text, remove_stop_words=remove_stop_words, max_words=max_words, 
                                size_largest_word=size_largest_word, image_width=image_width, random_state=random_state)
        st.pyplot(fig)
        
    with bar_chart_tab:
        # Generate bar chart
        fig = generate_bar_chart(text, remove_stop_words=remove_stop_words, min_word_count=min_word_count)
        st.pyplot(fig)
        
    with view_text_tab:
        # Show text
        st.write(text)
