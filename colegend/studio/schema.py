import graphene
from django.core.exceptions import ValidationError
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from colegend.api.models import CountableConnectionBase
from colegend.experience.models import add_experience
from colegend.home.models import get_controlled_habit, ControlledHabit
from colegend.scopes.models import Scope, get_scope_by_name
from colegend.scopes.schema import ScopeType
from colegend.journals.models import JournalEntry
from colegend.studio.filters import JournalEntryFilter
from .models import InterviewEntry, Chapter, Story


class JournalEntryNode(DjangoObjectType):
    end = graphene.Field(
        graphene.types.datetime.Date
    )

    class Meta:
        model = JournalEntry
        interfaces = [graphene.Node]
        connection_class = CountableConnectionBase

    def resolve_end(self, info):
        return self.end


class JournalEntryQuery(graphene.ObjectType):
    journal_entry = graphene.Node.Field(JournalEntryNode)
    journal_entries = DjangoFilterConnectionField(JournalEntryNode, filterset_class=JournalEntryFilter)
    journal_streak = graphene.Int()

    def resolve_journal_streak(self, info):
        user = info.context.user
        if user.is_authenticated:
            habit = get_controlled_habit(user, ControlledHabit.JOURNAL_HABIT)
            return habit.streak
        return 0


class AddJournalEntryMutation(graphene.relay.ClientIDMutation):
    journal_entry = graphene.Field(JournalEntryNode)

    class Input:
        scope = ScopeType()
        start = graphene.types.datetime.Date()
        keywords = graphene.String()
        content = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, scope=Scope.DAY.value, start=None, content='', keywords=''):
        user = info.context.user

        if not start:
            start = get_scope_by_name(scope)().start

        entry = user.journal_entries.create(scope=scope, start=start, content=content, keywords=keywords)

        # Updating streak
        today = timezone.localtime(timezone.now()).date()
        if entry.scope == Scope.DAY.value and entry.start == today:
            # Only update if this is today's day-entry.
            habit = get_controlled_habit(user, ControlledHabit.JOURNAL_HABIT)
            tracked = habit.track()
            if tracked:
                habit.save()
                add_experience(user, 'studio')
        return AddJournalEntryMutation(journal_entry=entry)


class UpdateJournalEntryMutation(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()
    journal_entry = graphene.Field(JournalEntryNode)

    class Input:
        id = graphene.ID()
        keywords = graphene.String()
        content = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, keywords=None, content=None):
        user = info.context.user
        _type, id = from_global_id(id)
        entry = user.journal_entries.get(id=id)
        if keywords is not None:
            entry.keywords = keywords
        if content is not None:
            entry.content = content
        entry.save()
        return UpdateJournalEntryMutation(success=True, journal_entry=entry)


class AddJournalEntryNoteMutation(graphene.relay.ClientIDMutation):
    journal_entry = graphene.Field(JournalEntryNode)

    class Input:
        scope = ScopeType()
        content = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, scope=Scope.DAY.value, content=''):
        user = info.context.user
        start = get_scope_by_name(scope)().start
        entry, created = user.journal_entries.get_or_create(scope=scope, start=start)
        if content:
            entry.content += '{prefix}{content}'.format(
                prefix='\n' if entry.content else '',
                content=content
            )
        entry.save()
        return AddJournalEntryNoteMutation(journal_entry=entry)


class JournalEntryMutation(graphene.ObjectType):
    add_journal_entry = AddJournalEntryMutation.Field()
    update_journal_entry = UpdateJournalEntryMutation.Field()
    add_journal_entry_note = AddJournalEntryNoteMutation.Field()


class InterviewEntryNode(DjangoObjectType):
    class Meta:
        model = InterviewEntry
        filter_fields = {
            'scope': ['exact'],
            'start': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }
        interfaces = [graphene.Node]


class InterviewEntryQuery(graphene.ObjectType):
    interview_entry = graphene.Node.Field(InterviewEntryNode)
    interview_entries = DjangoFilterConnectionField(InterviewEntryNode)


class AddInterviewEntry(graphene.relay.ClientIDMutation):
    interview_entry = graphene.Field(InterviewEntryNode)

    class Input:
        scope = ScopeType()
        start = graphene.types.datetime.Date()
        likes = graphene.String()
        dislikes = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, scope=Scope.DAY.value, start=None, likes='', dislikes=''):
        user = info.context.user
        if not start:
            start = timezone.localdate(timezone.now())
        entry = user.interview_entries.create(scope=scope, start=start, likes=likes, dislikes=dislikes)
        return AddInterviewEntry(interview_entry=entry)


class UpdateInterviewEntryMutation(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()
    interview_entry = graphene.Field(InterviewEntryNode)

    class Input:
        id = graphene.ID()
        likes = graphene.String()
        dislikes = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, likes=None, dislikes=None):
        user = info.context.user
        _type, id = from_global_id(id)
        entry = user.interview_entries.get(id=id)
        if likes:
            entry.likes = likes
        if dislikes:
            entry.dislikes = dislikes
        entry.save()
        return UpdateInterviewEntryMutation(success=True, interview_entry=entry)


class InterviewEntryMutation(graphene.ObjectType):
    add_interview_entry = AddInterviewEntry.Field()
    update_interview_entry = UpdateInterviewEntryMutation.Field()


class StoryNode(DjangoObjectType):
    class Meta:
        model = Story
        filter_fields = {
            'owner': ['exact'],
        }
        interfaces = [graphene.Node]


class StoryQuery(graphene.ObjectType):
    story = graphene.Node.Field(StoryNode)
    stories = DjangoFilterConnectionField(StoryNode)


class ChapterNode(DjangoObjectType):
    class Meta:
        model = Chapter
        filter_fields = {
            'name': ['exact', 'istartswith', 'icontains'],
            'content': ['exact', 'icontains'],
        }
        interfaces = [graphene.Node]


class ChapterQuery(graphene.ObjectType):
    chapter = graphene.Node.Field(ChapterNode)
    chapters = DjangoFilterConnectionField(ChapterNode)


class AddChapter(graphene.relay.ClientIDMutation):
    chapter = graphene.Field(ChapterNode)

    class Input:
        name = graphene.String()
        content = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, name='', content=''):
        user = info.context.user
        if not (name or content):
            raise ValidationError('Please provide at leat "name" or "content"')
        chapter = Chapter.objects.create(story=user.story, name=name, content=content)
        today = timezone.localtime(timezone.now()).date()
        if not user.story.chapters.filter(created__year=today.year, created__month=today.month).exists():
            add_experience(user, 'studio', 4)
        return AddChapter(chapter=chapter)


class UpdateChapterMutation(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()
    chapter = graphene.Field(ChapterNode)

    class Input:
        id = graphene.ID()
        name = graphene.String()
        content = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, name=None, content=None):
        user = info.context.user
        _type, id = from_global_id(id)
        chapter = user.story.chapters.get(id=id)
        if name is not None:
            chapter.name = name
        if content is not None:
            chapter.content = content
        chapter.save()
        return UpdateChapterMutation(success=True, chapter=chapter)


class DeleteChapterMutation(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()

    class Input:
        id = graphene.ID()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        user = info.context.user
        _type, id = from_global_id(id)
        chapter = user.story.chapters.get(id=id)
        chapter.delete()
        return DeleteChapterMutation(success=True)


class ChapterMutation(graphene.ObjectType):
    add_chapter = AddChapter.Field()
    update_chapter = UpdateChapterMutation.Field()
    delete_chapter = DeleteChapterMutation.Field()


class StudioQuery(
    InterviewEntryQuery,
    JournalEntryQuery,
    StoryQuery,
    ChapterQuery,
    graphene.ObjectType):
    pass


class StudioMutation(
    InterviewEntryMutation,
    JournalEntryMutation,
    ChapterMutation,
    graphene.ObjectType):
    pass
