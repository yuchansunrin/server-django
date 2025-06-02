from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from vote.models import Question


# Create your views here.
def index(request: HttpRequest):
    question_list = Question.objects.all()
    # 메세지 표시 (optional, create 페이지에서 질문 만든경우)
    created = request.GET.get("created", False)
    return render(
        request, "index.html",
        {"question_list": question_list, "created": created}
    )


def detail(request: HttpRequest, question_id: str):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "detail.html", {"question": question})


def vote(request: HttpRequest, question_id: str):
    question = get_object_or_404(Question, pk=question_id)
    selected_choice = question.choice_set.get(pk=request.POST["choice"])
    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(reverse("vote:results", args=(question.id,)))


def results(request: HttpRequest, question_id: str):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "results.html", {"question": question})


# Create a new question and its choices


def create(request: HttpRequest):
    if request.method == "POST":
        question = Question(
            question_text=request.POST["question_text"],
            expire_date=request.POST["expire_date"],
        )
        question.save()
        choices = request.POST.getlist("choices")
        print(choices)
        for choice_text in choices:
            question.choice_set.create(choice_text=choice_text, votes=0)
        return HttpResponseRedirect(reverse("vote:index") + "?created=True")
    else:
        return render(request, "create.html")
