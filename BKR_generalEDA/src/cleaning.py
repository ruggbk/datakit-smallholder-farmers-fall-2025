import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# -------------------------------------------------------------------
# Precompile regex patterns
# -------------------------------------------------------------------

RE_OPTOUT = re.compile(r"optout stop 6333", re.IGNORECASE)
RE_LEADING_NUM = re.compile(r"^\s*\d+\s+")
RE_ASKS = re.compile(r"^(?:[a-z\s]+ asks:)+\s*", re.IGNORECASE)
RE_Q_PREFIX = re.compile(r"^q[n]?\s*[:,-]?\s*")
RE_Q_WORD = re.compile(r"^q(?=[a-z])")
RE_REPLY_Q = re.compile(r"^reply\s+q[n]?\s*[:,-]?\s*", re.IGNORECASE)
RE_REPLY_FOLLOWED = re.compile(r"^reply\s+followed\s*", re.IGNORECASE)

RE_PUNCT = re.compile(r"[^\w\s]")
RE_STANDALONE_Q = re.compile(r"\bq\b")
RE_NUMBERS = re.compile(r"\d+")
RE_WHITESPACE = re.compile(r"\s+")

# -------------------------------------------------------------------
# Light preprocessing helpers
# -------------------------------------------------------------------

def strip_prefixes(text: str) -> str:
    """Remove boilerplate prefixes and common patterns."""
    text = text.lower()

    text = RE_OPTOUT.sub("", text)
    text = RE_LEADING_NUM.sub("", text)
    text = RE_ASKS.sub("", text)
    text = RE_Q_PREFIX.sub("", text)
    text = RE_Q_WORD.sub("", text)
    text = RE_REPLY_Q.sub("", text)
    text = RE_REPLY_FOLLOWED.sub("", text)

    return text.strip()


def clean_text(text: str) -> str:
    """
    Light cleaning: remove prefixes, punctuation, numbers, extra spaces.
    """
    text = strip_prefixes(text)
    text = text.lower()

    text = RE_PUNCT.sub("", text)
    text = RE_STANDALONE_Q.sub("", text)
    text = RE_NUMBERS.sub("num_token", text)
    text = RE_WHITESPACE.sub(" ", text)

    return text.strip()

# -------------------------------------------------------------------
# Tokenization + lemmatization
# -------------------------------------------------------------------

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def tokenize(text: str):
    return [w for w in text.split() if w not in stop_words]


def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(t) for t in tokens]




