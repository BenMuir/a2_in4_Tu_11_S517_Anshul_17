"""Semantic search for tournaments using sentence-transformers (all-MiniLM-L6-v2).

1. Each tournament's text is turned into an embedding and stored in the database
2-3. The user's search query is turned into an embedding with the same model
4. The query is compared to every stored embedding using cosine similarity
5-6. Tournaments are ranked from most to least similar and the best matches are shown
"""
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = 'all-MiniLM-L6-v2'

# Matches scoring below this are treated as unrelated and hidden
MIN_SCORE = 0.25

CATEGORY_LABELS = {
    'deck3v3': '3v3 Deck team tournament',
    'swiss1v1': '1v1 Swiss competitive tournament',
    'limited': 'Limited format tournament',
    'freeplay': 'Casual free-play meetup',
}

_model = None


def get_model():
    # Load the model the first time it is needed (it downloads once, then runs locally)
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def tournament_text(tournament):
    # The text that represents what a tournament is "about"
    entry = 'Free entry.' if tournament.price == 0 else f'Entry fee ${tournament.price}.'
    category = CATEGORY_LABELS.get(tournament.category, tournament.category)
    return f'{tournament.title}. {category}. {entry} Venue: {tournament.venue}. {tournament.description}'


def embed_tournament(tournament):
    # Step 1: generate the tournament's embedding and store it on the record (saved on commit)
    tournament.embedding = get_model().encode(tournament_text(tournament)).tolist()


def search(query, tournaments, limit=10):
    """Return (tournament, score) pairs ranked from best to worst match."""
    model = get_model()

    # Step 3: embed the user's query with the same model
    query_embedding = model.encode(query)

    # Older records may not have an embedding yet, so create any that are missing
    for t in tournaments:
        if t.embedding is None:
            embed_tournament(t)

    # Step 4: cosine similarity between the query and every stored tournament embedding
    scores = util.cos_sim(query_embedding, [t.embedding for t in tournaments])[0].tolist()

    # Step 5: rank from highest to lowest similarity, dropping weak matches
    ranked = sorted(zip(tournaments, scores), key=lambda pair: pair[1], reverse=True)
    return [(t, score) for t, score in ranked if score >= MIN_SCORE][:limit]
