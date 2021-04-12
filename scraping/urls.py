from django.urls import path

from . import views

urlpatterns = [
    # hook up the root URL with the project_index view
    # path("", views.project_index, name = "project_index"),
    path("table/", views.table_view, name="table"),
    path("results/", views.results_view, name="results"),
    path("fixtures/", views.fixtures_view, name="fixtures"),
    path("stats/", views.stats_view, name="stats"),
    path("pool/", views.pool_view, name = "pool")
    #path("stats/", views.stats, name = "epl_stats"),
    #path("fixtures/", views.fixtures, name = "epl_fixtures")
    # dynamically generate URL depending on the project you want to view
    # value passed in the URL is an integer and it's variable is pk
    # path("<int:pk>/", views.project_detail, name = "project_detail"),
    #path("<int:pk>/", views.job_detail, name="job_detail"),
]
