# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer, AnswerSerializer
from SPARQLWrapper import SPARQLWrapper, JSON

class QuestionListView(APIView):
    def get(self, request):
        questions = [
            {"id": i, "text": question}
            for i, question in enumerate(["Quelle est la capitale de l'Algérie?", ...])
        ]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class AnswerView(APIView):
    def get(self, request, question_id):
        questions = ["Quelle est la capitale de l'Algérie?", ...]

        # Define SPARQL queries directly in the view
        if question_id == 0:
            query = """
            SELECT ?capital
            WHERE {
              ?country rdf:type dbo:Country ;
                       rdfs:label "Algérie"@fr ;
                       dbo:capital ?capitalResource .
              ?capitalResource rdfs:label ?capital .
              FILTER(LANG(?capital) = 'fr')
            }
            """
        # Add other SPARQL queries for different questions here

        results = execute_sparql_query(query)
        answer = get_answer_from_results(results)

        serializer = AnswerSerializer({"question_id": question_id, "answer": answer})
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_answer_from_results(results):
    answers = []
    for result in results["results"]["bindings"]:
        answers.append(result["capital"]["value"])
    return answers

def execute_sparql_query(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results