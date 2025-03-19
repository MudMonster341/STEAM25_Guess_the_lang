import random
from django.shortcuts import render, redirect

# List of languages. (Internal names should match your image naming convention)
LANGUAGES = [
    "Python", "Java", "JavaScript", "HTML", "C", "C++", "Csharp", "R",
    "Rust", "Assembly", "SQL", "PHP", "Ruby", "Swift", "Go"
]

# Mapping of internal names to display names
DISPLAY_NAMES = {
    "Csharp": "C#",
    # Add other mappings if needed
}

def home(request):
    """
    Home page view that displays a start button.
    """
    # Initialize score and question count when starting the game
    request.session['score'] = 0
    request.session['question_count'] = 0
    return render(request, "game/home.html")

def game(request):
    """
    Game view: Displays a code snippet image and multiple-choice options.
    If the form is submitted (or the timer runs out), it reloads a new question.
    """
    # Ensure the score and question count are initialized
    if 'score' not in request.session:
        request.session['score'] = 0
    if 'question_count' not in request.session:
        request.session['question_count'] = 0

    if request.method == "POST":
        # Check if the answer is correct (submitted value is internal value)
        selected_choice = request.POST.get('choice')
        correct_language = request.session.get('correct_language')
        
        # Debug prints
        print(f"Selected choice: {selected_choice}, type: {type(selected_choice)}")
        print(f"Correct language: {correct_language}, type: {type(correct_language)}")
        print(f"Current score: {request.session.get('score', 0)}")
        
        if selected_choice == correct_language:
            # Get current score and add 10
            new_score = request.session.get('score', 0) + 10
            request.session['score'] = new_score
            # Explicitly mark the session as modified
            request.session.modified = True
            print(f"Score updated to: {new_score}")

        # Increment question count
        request.session['question_count'] += 1

        # Check if 10 questions have been answered
        if request.session['question_count'] >= 10:
            return redirect('final_score')

        return redirect('game')

    # Randomly select a correct language and one of its three snippet images
    correct_language = random.choice(LANGUAGES)
    snippet_number = random.choice([1, 2, 3])
    image_filename = f"{correct_language}_{snippet_number}.png"  # images like Python_1.png

    # Create a list of internal options (correct + three random distractors)
    options_internal = [correct_language] + random.sample([lang for lang in LANGUAGES if lang != correct_language], 3)
    random.shuffle(options_internal)

    # Create options as a list of dictionaries with internal and display values.
    options = [
        {'value': option, 'display': DISPLAY_NAMES.get(option, option)}
        for option in options_internal
    ]

    # Store the correct language (internal value) in the session
    request.session['correct_language'] = correct_language

    context = {
        "image_filename": image_filename,
        "options": options,  # Each option now has 'value' and 'display'
        "score": request.session.get('score', 0),
        "correct_language": correct_language,  # For JavaScript highlighting
    }
    return render(request, "game/game.html", context)

def final_score(request):
    """
    Final score view: Displays the player's final score out of 100.
    """
    score = request.session.get('score', 0)
    return render(request, "game/final_score.html", {"score": score})
