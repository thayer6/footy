from django.shortcuts import render

from scraping.models import ResultsFixtures, Table, Stats, PoolTable

def table_view(request):
    table = Table.objects.all()
    return render(request,'table.html',{'table':table})

def results_view(request):
    results = ResultsFixtures.objects.exclude(score="")
    return render(request, 'results.html',{'results':results})

def fixtures_view(request):
    fixtures = ResultsFixtures.objects.filter(score="")
    return render(request, 'fixtures.html', {'fixtures':fixtures})

def stats_view(request):
    stats = Stats.objects.all()
    return render(request, 'stats.html', {'stats':stats})

def pool_view(request):
    pool = PoolTable.objects.all()
    pool = pool.order_by('-points')
    return render(request, 'pool.html', {'pool':pool})

# # import the get_user_model
# # User = get_user_model()


# # user_search = list(User.objects.value_list(jobs_of_interest, flat = True))
# # jobs = Job.objects.filter(searched_job=user_search, )
# # for loop to loop through user_search if error thrown from filter

# # Create your views here.
# def job_index(request):
#     # queryset to return all job objects
#     # TODO: return only the jobs that are specific to the user
#     # user_search = list(User.objects.value_list(jobs_of_interest, flat = True))
#     # jobs = list(Job.objects.filter(job_searched = user_search))
#     # error may be thrown here, if so loop through user_search to filter job_searched
#     jobs = Job.objects.all()
#     context = {"jobs": jobs}

#     return render(request, "job_index.html", context)


# def job_detail(request, pk):
#     job = Job.objects.get(pk=pk)
#     context = {"job": job}
#     return render(request, "job_detail.html", context)
