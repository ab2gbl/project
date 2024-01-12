# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer, AnswerSerializer
from SPARQLWrapper import SPARQLWrapper, JSON
import json
class QuestionListView(APIView):
    def get(self, request):
        questions = [
            {"id": i, "text": question}
            for i, question in enumerate(["Quelle est la capitale de l'Algérie ?", 
                     "Quelle est la deuxième plus grande ville en Algérie en termes de population ?",
                     "Quels acteurs sont nés en 2003 ?",
                     "Donnez-moi le plus gros livre, l'auteur, le nombre de pages, et le nom en arabe s'il existe?",
                     "the tallest mountain between algeria and france",
                     "Quel est le nom de la plus grande ville en France ou en Italie, où la population est supérieure à un million ?",
                     " Quel est le premier film sorti en 2010  ?",
                     "Pouvez-vous me donner des films algériens ?",
                     "Quels sont les artistes originaires d'Algérie et ayant produit des œuvres artistiques ?",
                     
                     
                     ...])
        ]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class AnswerView(APIView):
    def get(self, request, question_id):
        questions = ["Quelle est la capitale de l'Algérie ?", 
                     "Quelle est la deuxième plus grande ville en Algérie en termes de population ?",
                     "Quels acteurs sont nés en 2003 ?",
                     "Donnez-moi le plus gros livre, l'auteur, le nombre de pages, et le nom en arabe s'il existe?",
                     "the tallest mountain between algeria and france",
                     "Quel est le nom de la plus grande ville en France ou en Italie, où la population est supérieure à un million ?",
                     " Quel est le premier film sorti en 2010  ?",
                     "Pouvez-vous me donner des films algériens ?",
                     "Quels sont les artistes originaires d'Algérie et ayant produit des œuvres artistiques ?",
                     
                     
                     ...]

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
        if question_id == 1:
            query ="""
            PREFIX dbo: <http://dbpedia.org/ontology/>

            SELECT ?cityName ?population WHERE {
            ?city a dbo:City ;
                    dbo:country dbr:Algeria ;
                    rdfs:label ?cityName ;
                    dbo:populationTotal ?population .
            FILTER(LANG(?cityName) = "en")
            }
            ORDER BY DESC(?population)
            LIMIT 1 OFFSET 1
            
            """    
        if question_id == 2:
            query ="""
             SELECT ?actor ?Name ?birthDate
            WHERE {
            ?actor rdf:type dbo:Actor ;
                    dbo:birthDate ?birthDate ;
                    rdfs:label ?Name .
            FILTER (LANG(?Name) = 'en' && YEAR(?birthDate) = 2003)
            }
            LIMIT 1

            
            """    
        if question_id == 3:
            query ="""
            SELECT ?englishWriter ?englishWork (SUM(?numPages) AS ?totalPages) ?arabicName
            WHERE {
            ?writer rdf:type dbo:Writer ;
                    dbo:notableWork ?work .
            ?work dbo:numberOfPages ?numPages .
            ?writer rdfs:label ?englishWriter .
            FILTER(LANG(?englishWriter) = 'en')
            ?work rdfs:label ?englishWork .
            FILTER(LANG(?englishWork) = 'en')
            OPTIONAL {
                ?work rdfs:label ?arabicName .
                FILTER(LANG(?arabicName) = 'ar')
            }
            }
            GROUP BY ?englishWriter ?englishWork ?arabicName
            ORDER BY DESC(?totalPages)
            LIMIT 1 
            
            """
            
        if question_id == 4:
            query ="""
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?countryLabel ?mountainLabel ?elevation WHERE {
                {
                    SELECT dbr:Algeria AS ?country ?mountain ?elevation ?countryLabel ?mountainLabel WHERE {
                    ?mountain a dbo:Mountain ;
                                dbo:locatedInArea dbr:Algeria ;
                                dbo:elevation ?elevation .
                    OPTIONAL { dbr:Algeria rdfs:label ?countryLabel FILTER(LANG(?countryLabel) = "en") }
                    OPTIONAL { ?mountain rdfs:label ?mountainLabel FILTER(LANG(?mountainLabel) = "en") }
                    }
                    ORDER BY DESC(?elevation)
                    LIMIT 1
                }
                UNION
                {
                    SELECT dbr:France AS ?country ?mountain ?elevation ?countryLabel ?mountainLabel WHERE {
                    ?mountain a dbo:Mountain ;
                                dbo:locatedInArea dbr:France ;
                                dbo:elevation ?elevation .
                    OPTIONAL { dbr:France rdfs:label ?countryLabel FILTER(LANG(?countryLabel) = "en") }
                    OPTIONAL { ?mountain rdfs:label ?mountainLabel FILTER(LANG(?mountainLabel) = "en") }
                    }
                    ORDER BY DESC(?elevation)
                    LIMIT 1
                }
                }
                ORDER BY DESC(?elevation)
                LIMIT 1
            """   
            
        if question_id == 5:
            query ="""
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?cityName WHERE {
                ?city a dbo:City ;
                        rdfs:label ?cityName ;
                        dbo:populationTotal ?population ;
                        dbo:country ?country .
                FILTER(LANG(?cityName) = "en" && (?country = dbr:France || ?country = dbr:Italy) && ?population > 1000000)
                }
                ORDER BY DESC(?population)
                LIMIT 1

            """ 
            
        if question_id == 6:
            query ="""  
                SELECT ?film ?englishName ?releaseDate
                WHERE {
                ?film rdf:type dbo:Film ;
                        rdfs:label ?englishName ;
                        dbo:releaseDate ?releaseDate .
                FILTER (LANG(?englishName) = 'en' && YEAR(?releaseDate) = 2010)
                }
                ORDER BY ?releaseDate
                LIMIT 1
            """ 
    
        if question_id == 7:
                query ="""
            SELECT ?film ?filmTitle
            WHERE {
            ?film rdf:type dbo:Film ;
                    dbo:country dbr:Algeria ;
                    rdfs:label ?filmTitle .
            FILTER (LANG(?filmTitle) = 'en')
            }
            LIMIT 10

            """
            
        if question_id == 8:
                        query ="""
                        SELECT ?artist ?artistName 
            WHERE {
            ?artist rdf:type dbo:Artist ;
                    dbo:birthPlace dbr:Algeria ;
                    rdfs:label ?artistName .
            FILTER (LANG(?artistName) = 'en')
            }
            LIMIT 10



            """
        # Add other SPARQL queries for different questions here

        results = execute_sparql_query(query)
        answer = get_answer_from_results(question_id,results)

        serializer = AnswerSerializer({"question_id": question_id, "answer": answer})
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_answer_from_results(question_id,results):
    answers = []
    for result in results["results"]["bindings"]:
        if question_id == 0:
            answers.append(result["capital"]["value"])
        elif question_id == 1:
            answers.append(result["cityName"]["value"])
            #answers.append(result["population"]["value"])
        elif question_id == 2:
            answers.append(result["Name"]["value"])
        elif question_id == 3:
                if ('arabicName' in result):
                    answers.append({
                        'Writer': result['englishWriter']['value'],
                        'Work': result['englishWork']['value'],
                        'totalPages': result['totalPages']['value'],
                        'ArabicName':  result['arabicName']['value'],
                    })
                else :
                    answers.append({
                        'Writer': result['englishWriter']['value'],
                        'Work': result['englishWork']['value'],
                        'totalPages': result['totalPages']['value'],
                        
                    })
        elif question_id == 4: 
                answers.append({
                    'countryLabel': result['countryLabel']['value'],
                    'mountainLabel': result['mountainLabel']['value'],
                    'elevation': result['elevation']['value'],
                })
        elif question_id == 5:
            answers.append(result["cityName"]["value"])
        elif question_id == 6:
            answers.append(result["englishName"]["value"])
        elif question_id == 7:
            answers.append(result["filmTitle"]["value"])
            
        elif question_id == 8:
            answers.append(result["artistName"]["value"])
            
            
        
    return answers

def execute_sparql_query(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results