"""Check lecturer-required external facts without inventing contribution records."""
import math
from urllib.parse import urlparse

def readiness_issues(meta):
    issues=[]
    if meta.get('dataset_approved') is not True:issues.append('Dataset registration/lecturer acceptance not confirmed')
    parsed=urlparse(meta.get('youtube_url') or '')
    if parsed.scheme!='https' or parsed.hostname not in {'youtube.com','www.youtube.com','youtu.be','www.youtu.be'} or parsed.path in {'','/'}:
        issues.append('Actual YouTube report URL missing or invalid')
    duration=meta.get('video_duration_seconds')
    if isinstance(duration,bool) or not isinstance(duration,(int,float)) or not 420<=duration<=900:
        issues.append('Actual video duration must be confirmed within 420–900 seconds')
    if meta.get('contributions_confirmed') is not True:issues.append('Actual contribution records not confirmed by group')
    shares=[]
    for author in meta.get('authors',[]):
        if not isinstance(author.get('tasks'),str) or not author['tasks'].strip():issues.append(f"{author['id']}: actual tasks missing")
        for key in ['contribution_percent','completion_percent']:
            value=author.get(key)
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 0<=value<=100:
                issues.append(f"{author['id']}: {key} missing/invalid")
        shares.append(author.get('contribution_percent'))
    if all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in shares) and shares and not math.isclose(sum(shares),100,abs_tol=.01):
        issues.append('Actual contribution percentages must sum to 100')
    return issues
