from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id = "bvqn22c354gnxrv7",
        public_key = "9q28xvnvsn9vzcbs",
        private_key = "420c50cf5c830fce9e52e801286d1a30"
    )
)


def validate_user_session(id,token):
    UserModel = get_user_model()
    
    try:
        user = UserModel.object.get(pk = id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExit:
        return False
    
@csrf_exempt
def generate_token(request,id, token):
    if not validate_user_session(id,token):
        return JsonResponse({'error': 'Invalid session, Please login again !'})
    return JsonResponse({'clientToken' :gateway.client_token.generate(),'success':True})

@csrf_exempt
def process_payment(request,id, token):
    if not validate_user_session(id,token):
        return JsonResponse({'error': 'Invalid session, Please login again !'})
    
    nonce_from_the_client = request.POST['paymentMethodNonce']
    amount_from_the_client = request.POST['amount']
    
    result = gateway.transaction.sale({
        'amount': amount_from_the_client,
        'payment_method_nonce' : nonce_from_the_client,
        'option' :{
            "submit_for_settlement" : True
        }
    })


    if result.is_success:
        return JsonResponse({
            "success" : result.is_success,"transaction" :{'id' :result.transaction.id,'amount' : result.transaction.amount}})
    
    else:
        return JsonResponse({'error': True,'sucess': False})
    