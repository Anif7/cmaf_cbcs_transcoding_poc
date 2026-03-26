import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from app.models import TranscodingJob
from app.tasks.transcoding import run_transcoding_pipeline

@method_decorator(csrf_exempt, name='dispatch')
class TranscodingTriggerView(View):
    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body)
            
            input_url = payload.get('input_url')
            output_url = payload.get('output_url')
            webhook_url = payload.get('webhook_url')
            storage_params = payload.get('storage_parameters', {})
            drm_encryption = payload.get('drm_encryption', {})
            
            raw_meta = payload.get('meta_data', {})
            meta_data = json.loads(raw_meta) if isinstance(raw_meta, str) else raw_meta
            
            meta_data['settings'] = payload.get('settings', {})
            
            transcoding_job = TranscodingJob.objects.create(
                input_url=input_url,
                output_path=output_url,
                webhook_url=webhook_url,
                storage_config=storage_params,
                drm_config=drm_encryption,
                meta_data=meta_data
            )
            
            run_transcoding_pipeline.delay(transcoding_job.id)
            
            return JsonResponse({
                'id': transcoding_job.id, 
                'status': transcoding_job.get_status_display()
            }, status=201)
        except Exception as trigger_error:
            return JsonResponse({'error': str(trigger_error)}, status=400)
