from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.contenttypes.models import ContentType

from kitsune.kbforums.feeds import ThreadsFeed, PostsFeed
from kitsune.kbforums.models import Post
from kitsune.flagit import views as flagit_views
from kitsune.sumo.views import handle404


if settings.DISABLE_FEEDS:
    threads_feed_view = handle404
    posts_feed_view = handle404
else:
    threads_feed_view = ThreadsFeed()
    posts_feed_view = PostsFeed()

# These patterns inherit from /document/discuss
urlpatterns = patterns(
    'kitsune.kbforums.views',
    url(r'^$', 'threads', name='wiki.discuss.threads'),
    url(r'^feed', threads_feed_view, name='wiki.discuss.threads.feed'),
    url(r'^new', 'new_thread', name='wiki.discuss.new_thread'),
    url(r'^watch', 'watch_forum', name='wiki.discuss.watch_forum'),
    url(r'^post-preview-async$', 'post_preview_async',
        name='wiki.discuss.post_preview_async'),
    url(r'^(?P<thread_id>\d+)$', 'posts', name='wiki.discuss.posts'),
    url(r'^(?P<thread_id>\d+)/feed$', posts_feed_view,
        name='wiki.discuss.posts.feed'),
    url(r'^(?P<thread_id>\d+)/watch$', 'watch_thread',
        name='wiki.discuss.watch_thread'),
    url(r'^(?P<thread_id>\d+)/reply$', 'reply', name='wiki.discuss.reply'),
    url(r'^(?P<thread_id>\d+)/sticky$', 'sticky_thread',
        name='wiki.discuss.sticky_thread'),
    url(r'^(?P<thread_id>\d+)/lock$', 'lock_thread',
        name='wiki.discuss.lock_thread'),
    url(r'^(?P<thread_id>\d+)/edit$', 'edit_thread',
        name='wiki.discuss.edit_thread'),
    url(r'^(?P<thread_id>\d+)/delete$', 'delete_thread',
        name='wiki.discuss.delete_thread'),
    url(r'^(?P<thread_id>\d+)/(?P<post_id>\d+)/edit', 'edit_post',
        name='wiki.discuss.edit_post'),
    url(r'^(?P<thread_id>\d+)/(?P<post_id>\d+)/delete', 'delete_post',
        name='wiki.discuss.delete_post'),
    # Flag discussion posts
    url(r'^(?P<object_id>\d+)/flag$', flagit_views.flag,
        {'content_type': ContentType.objects.get_for_model(Post).id},
        name='wiki.discuss.flag_post'),
)
