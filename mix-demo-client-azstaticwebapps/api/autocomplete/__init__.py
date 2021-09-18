import logging
import azure.functions as func
import json
from azure_services import CognitiveSearchApi

# https://docs.microsoft.com/en-us/rest/api/searchservice/autocomplete#query-parameters
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body     = req.get_json()
        search_text  = req_body.get('q', None)
        suggester    = req_body.get('suggester', 'sg')
        mode         = req_body.get('mode', 'oneTermWithContext') # oneTerm, twoTerms, oneTermWithContext
        post_tag     = req_body.get('post_tag', '%3A')
        pre_tag      = req_body.get('pre_tag', '%3A')
        min_coverage = req_body.get('min_coverage', 50)
        top          = req_body.get('top', 3)
        fields       = req_body.get('search_fields', None) # list
    except ValueError:
        search_text  = req.params.get('q', None)
        suggester    = req.params.get('suggester', 'sg')
        mode         = req.params.get('mode', 'oneTermWithContext') # oneTerm, twoTerms, oneTermWithContext
        post_tag     = req.params.get('post_tag', '%3A')
        pre_tag      = req.params.get('pre_tag', '%3A')
        min_coverage = req.params.get('min_coverage', 50)
        top          = req.params.get('top', 3)
        fields       = req.params.get('search_fields', None) # list


    if search_text:
        suggestions = CognitiveSearchApi().autocomplete(search_text=search_text, suggester=suggester, mode=mode, post_tag=post_tag, pre_tag=pre_tag, min_coverage=min_coverage, top=top, fields=fields)
        """
        if (len(suggestions) == 0 and ' ' in search_text):
            search_text = search_text.split(' ').pop()
            suggestions = CognitiveSearchApi().autocomplete(search_text=search_text, suggester=suggester, mode=mode, post_tag=post_tag, pre_tag=pre_tag, min_coverage=min_coverage, top=top, fields=fields)
        """
        return func.HttpResponse(body=json.dumps(suggestions), mimetype="application/json",status_code=200)
    else:
        return func.HttpResponse(
             "No query param 'q' found.",
             status_code=200
        )
