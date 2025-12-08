import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# -------------------------------------------------------------------
# Minimal cleaning
# -------------------------------------------------------------------

def minimal_clean(text):
    # Normalize spacing
    text = re.sub(r'\s+', ' ', text).strip()
    # Optional: remove common prefixes
    text = re.sub(r'^(Q[:.]?|QA [^:]+ asks:)\s*', '', text, flags=re.IGNORECASE)
    return text

# -------------------------------------------------------------------
# Precompile regex patterns
# -------------------------------------------------------------------

# Remove opt-out phrases, including variants like "OptOut*196#"
RE_OPTOUT = re.compile(r"optout.*?\d*", re.IGNORECASE)

# Leading numbers (e.g., question IDs at start of text)
RE_LEADING_NUM = re.compile(r"^\s*\d+\s+")

# Nested or multiple "asks:" chains
RE_ASKS = re.compile(r"(?:[a-zA-Z\s]+\s+asks[:\?]*)+", re.IGNORECASE)

# Remove all forms of Q<num> references, optionally prefixed by "Reply"
RE_Q_NUM = re.compile(r"(?:reply\s+)?q[\.:,-]?\d+", re.IGNORECASE)
RE_Q_NUM = re.compile(r"(?:reply\s+)?q[:\.\-]?\d+(?:\s+followed by your response)?", re.IGNORECASE)

# Remove generic "q" words followed by letters (e.g., qwhat)
RE_Q_WORD = re.compile(r"q(?=[a-z])", re.IGNORECASE)
RE_Q_WORD_SAFE = re.compile(r"\bq(what|how|where|which|who)\b", re.IGNORECASE)

# Remove "reply followed" boilerplate
RE_REPLY_FOLLOWED = re.compile(r"reply\s+followed\s*", re.IGNORECASE)

# Punctuation, standalone q, numbers, and whitespace
RE_PUNCT = re.compile(r"[^\w\s]")
RE_STANDALONE_Q = re.compile(r"\bq\b")
RE_NUMBERS = re.compile(r"\d+")
RE_WHITESPACE = re.compile(r"\s+")

# -------------------------------------------------------------------
# Light preprocessing helpers
# -------------------------------------------------------------------

def strip_prefixes(text: str) -> str:
    """Remove boilerplate prefixes and common patterns."""
    text = RE_OPTOUT.sub("", text)
    text = RE_LEADING_NUM.sub("", text)
    text = RE_ASKS.sub("", text)
    text = RE_Q_NUM.sub("", text)
    text = RE_Q_WORD_SAFE.sub("", text)
    text = RE_REPLY_FOLLOWED.sub("", text)

    return text.strip()


def clean_text(text: str) -> str:
    """
    Light cleaning: remove prefixes, punctuation, numbers, extra spaces.
    """
    text = strip_prefixes(text)

    # Replace inline numbers with num_token
    text = RE_NUMBERS.sub("num_token", text)

    # Remove punctuation and standalone "q"
    text = RE_PUNCT.sub("", text)
    text = RE_STANDALONE_Q.sub("", text)

    # Collapse multiple spaces
    text = RE_WHITESPACE.sub(" ", text)

    return text.strip()

# -------------------------------------------------------------------
# Tokenization + lemmatization
# -------------------------------------------------------------------

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def tokenize(text: str):
    text = text.lower()
    return [w for w in text.split() if w not in stop_words]


def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(t) for t in tokens]




