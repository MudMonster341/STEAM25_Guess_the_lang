import random
from django.shortcuts import render, redirect

# List of languages. (Internal names should match your image naming convention)
LANGUAGES = [
    "Python", "java", "JavaScript", "html", "C", "C++", "Csharp", "R",
    "RUST", "Assembly", "SQL", "php", "Ruby", "Swift", "GO"
]

# Mapping of internal names to display names
DISPLAY_NAMES = {
    "Python": "Python",
    "java": "Java",
    "JavaScript": "JavaScript",
    "html": "HTML",
    "C": "C",
    "C++": "C++",
    "Csharp": "C#",
    "R": "R",
    "RUST": "Rust",
    "Assembly": "Assembly",
    "SQL": "SQL",
    "php": "PHP",
    "Ruby": "Ruby",
    "Swift": "Swift",
    "GO": "Go"
}

def home(request):
    """
    Home page view that displays a start button.
    Resets the score, question count, and used_images list.
    """
    request.session['score'] = 0
    request.session['question_count'] = 0
    request.session['used_images'] = []  # Keep track of shown images
    return render(request, "game/home.html")

def game(request):
    """
    Game view: Presents a new question or processes a submitted answer.
    Avoids repeating snippet images by checking 'used_images' in session.
    """
    # Ensure the score, question_count, and used_images are in session
    if 'score' not in request.session:
        request.session['score'] = 0
    if 'question_count' not in request.session:
        request.session['question_count'] = 0
    if 'used_images' not in request.session:
        request.session['used_images'] = []

    if request.method == "POST":
        # Check if the answer is correct
        selected_choice = request.POST.get('choice')
        correct_language = request.session.get('correct_language')

        if selected_choice == correct_language:
            new_score = request.session['score'] + 10
            request.session['score'] = new_score
            request.session.modified = True

        # Increment question count
        request.session['question_count'] += 1

        # If 10 questions have been answered, go to final score
        if request.session['question_count'] >= 10:
            return redirect('final_score')
        else:
            return redirect('game')

    # ============= Generate a new question (GET request) =============

    used_images = request.session['used_images']

    # Keep picking a random snippet until we find one not used
    while True:
        correct_language = random.choice(LANGUAGES)
        snippet_number = random.choice([1, 2, 3])
        image_filename = f"{correct_language}_{snippet_number}.png"
        
        if image_filename not in used_images:
            # Found a snippet that hasn't been shown yet
            used_images.append(image_filename)
            request.session['used_images'] = used_images
            request.session.modified = True
            break
        # else: keep trying

    # Build a list of options: correct answer + 3 distractors
    options_internal = [correct_language] + random.sample(
        [lang for lang in LANGUAGES if lang != correct_language],
        3
    )
    random.shuffle(options_internal)

    # Convert internal values to display names
    options = [
        {'value': lang, 'display': DISPLAY_NAMES.get(lang, lang)}
        for lang in options_internal
    ]

    # Store the correct answer in session
    request.session['correct_language'] = correct_language

    context = {
        "image_filename": image_filename,
        "options": options,
        "score": request.session['score'],
        "correct_language": correct_language,
        "question_number": request.session['question_count'] + 1,
        "total_questions": 10,
    }
    return render(request, "game/game.html", context)

def final_score(request):
    """
    Final score view: Displays the player's final score out of 100.
    """
    score = request.session.get('score', 0)
    return render(request, "game/final_score.html", {"score": score})
