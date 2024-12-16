from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from rest_framework import viewsets
from .serializers import PostSerializer
from .forms import PostForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class BlogImages(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        post = Post.objects.get(pk=response.data['id'])

        if post.helmet_status == "not_wearing":
            self.send_helmet_alert()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        post = Post.objects.get(pk=response.data['id'])

        if post.helmet_status == "not_wearing":
            self.send_helmet_alert()
        return response

    @staticmethod
    def send_helmet_alert():
        print("send_helmet_alert")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": "Failure to wear a helmet has been detected!",
            },
        )

def post_list(request):
    print("post_list")
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    print("post_detail")
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    print("post_new")
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print(f"Helmet Status: {post.helmet_status}")
            # 헬멧 상태 확인 후 알림 전송
            # if post.helmet_status == "not_wearing":
            #     send_helmet_alert()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    print("post_edit")
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print(f"Helmet Status: {post.helmet_status}")
            # 헬멧 상태 확인 후 알림 전송
            # if post.helmet_status == "not_wearing":
            #     send_helmet_alert()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def js_test(request):
    print("js_test")
    return render(request, 'blog/js_test.html')

# def send_helmet_alert():
#     print("send_helmet_alert")
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "notifications",  # Notification 그룹
#         {
#             "type": "send_notification",  # 컨슈머의 메서드 이름
#             "message": "헬멧 미착용이 감지되었습니다!",  # 알림 메시지
#         },
#     )
    
