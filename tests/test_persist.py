from pyquerytracker import TrackQuery


@TrackQuery()
def sample_query():
    return "DB test successful"


sample_query()
