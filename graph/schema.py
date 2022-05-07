import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Book, Quizzes, Category, Question, Answer


class BooksType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id","title","excerpt")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id","name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id","title","category","date_created")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title","quiz","difficulty")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer_text")


class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType)
    quiz = graphene.String()
    all_quizzes = DjangoListField(QuizzesType)
    category = DjangoListField(CategoryType)
    all_questions = DjangoListField(QuestionType)
    fetch_Quiz = graphene.Field(QuizzesType,id=graphene.Int())
    fetch_Answer = graphene.List(AnswerType,id=graphene.Int())

    def resolve_all_books(root,info):
        return Book.objects.all()

    def resolve_quiz(root, info):
        return "This is a quiz string."

    def resolve_all_questions(root, info):
        return Question.objects.all()

    def resolve_fetch_Quiz(root,info,id):
        return Quizzes.objects.get(pk=id)

    def resolve_fetch_Answer(root,info,id):
        return Answer.objects.filter(question=id)

class AddCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate( cls,root, info, name):
        category = Category(name=name)
        category.save()
        return AddCategoryMutation(category=category)

class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate( cls,root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return UpdateCategoryMutation(category=category)

class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    success = graphene.String()

    @classmethod
    def mutate( cls, root, info, id):
        category = Category.objects.get(pk=id)
        category.delete()
        return DeleteCategoryMutation(success="Deleted Successfully")

class Mutation(graphene.ObjectType):
    add_category = AddCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)