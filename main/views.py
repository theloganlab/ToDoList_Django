from django.shortcuts import render, redirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.
def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():

        if response.method == "POST":
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    txt_subs = response.POST.get("txt#" + str(item.id))
                    item.text = txt_subs
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    
                    item.save()
            
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")\

            else:
                for item in ls.item_set.all():
                    if response.POST.get("delete" + str(item.id)) == "delete":
                        item.delete()

        return render(response, "main/list.html", {"ls":ls})
    
    return render(response, "main/view.html", {})

def home(response):
    count = 0
    if response.user.is_authenticated:
    
        count = len(response.user.todolist.all())


    return render(response, "main/home.html", {"count": count})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
    
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

        return redirect(f"/{t.id}")
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form": form})

def view(response):
    return render(response, "main/view.html", {})

