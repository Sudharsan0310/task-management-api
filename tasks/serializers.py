from rest_framework import serializers
from .models import Task, Category, Tag, Comment, Attachment
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Attachment
        fields = [
            'id', 'task', 'file', 'filename',
            'file_size', 'uploaded_by', 'uploaded_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at']

class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False)
    
    categories = CategorySerializer(many=True, read_only=True, source='taskcategory_set.category')
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    tags = TagSerializer(many=True, read_only=True, source='tasktag_set.tag')
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'due_date', 'owner', 'assigned_to', 'assigned_to_id',
            'categories', 'category_ids', 'tags', 'tag_ids',
            'comments', 'attachments',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'completed_at']
    
    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        tag_ids = validated_data.pop('tag_ids', [])
        
        task = Task.objects.create(**validated_data)
        
        # Add categories
        from .models import TaskCategory
        for category_id in category_ids:
            TaskCategory.objects.create(task=task, category_id=category_id)
        
        # Add tags
        from .models import TaskTag
        for tag_id in tag_ids:
            TaskTag.objects.create(task=task, tag_id=tag_id)
        
        return task
    
    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', None)
        tag_ids = validated_data.pop('tag_ids', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update categories if provided
        if category_ids is not None:
            from .models import TaskCategory
            TaskCategory.objects.filter(task=instance).delete()
            for category_id in category_ids:
                TaskCategory.objects.create(task=instance, category_id=category_id)
        
        # Update tags if provided
        if tag_ids is not None:
            from .models import TaskTag
            TaskTag.objects.filter(task=instance).delete()
            for tag_id in tag_ids:
                TaskTag.objects.create(task=instance, tag_id=tag_id)
        
        return instance

class TaskListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    assigned_to = serializers.StringRelatedField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'status', 'priority',
            'due_date', 'owner', 'assigned_to', 'created_at'
        ]
