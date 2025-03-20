import random
from django.shortcuts import render, redirect
from accounts.models import PlayerProfile  # Import at the top
from django.contrib.auth.decorators import login_required  # Newly added import
from django.urls import reverse

# List of languages. (Internal names should match your image naming convention)
LANGUAGES = [
    "Python", "java", "JavaScript", "html", "C", "C++", "Csharp", "R",
    "RUST", "Assembly", "SQL", "php", "Ruby", "Swift", "GO"
]

# Mapping of internal names to display names
DISPLAY_NAMES = {
    "Python": "Python",
    "java": "java",
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

@login_required(login_url='/accounts/login/')
def game(request):
    profile = PlayerProfile.objects.get(user=request.user)

    # If the user has already played, redirect to login page with ?already_played=true
    if profile.has_played:
        return redirect(f"{reverse('login')}?already_played=true")

    # === Existing game logic ===
    if 'score' not in request.session:
        request.session['score'] = 0
    if 'question_count' not in request.session:
        request.session['question_count'] = 0
    if 'used_images' not in request.session:
        request.session['used_images'] = []

    if request.method == "POST":
        selected_choice = request.POST.get('choice')
        correct_language = request.session.get('correct_language')

        if selected_choice == correct_language:
            request.session['score'] += 10
            request.session.modified = True

        request.session['question_count'] += 1
        if request.session['question_count'] >= 10:
            return redirect('final_score')
        else:
            return redirect('game')

    used_images = request.session['used_images']
    while True:
        correct_language = random.choice(LANGUAGES)
        snippet_number = random.choice([1, 2, 3])
        image_filename = f"{correct_language}_{snippet_number}.png"
        if image_filename not in used_images:
            used_images.append(image_filename)
            request.session['used_images'] = used_images
            request.session.modified = True
            break

    options_internal = [correct_language] + random.sample(
        [lang for lang in LANGUAGES if lang != correct_language],
        3
    )
    random.shuffle(options_internal)

    options = [
        {'value': lang, 'display': DISPLAY_NAMES.get(lang, lang)}
        for lang in options_internal
    ]

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
    score = request.session.get('score', 0)
    if request.user.is_authenticated:
        profile = PlayerProfile.objects.get(user=request.user)
        if not profile.has_played:
            profile.has_played = True
            profile.save()
    return render(request, "game/final_score.html", {"score": score})