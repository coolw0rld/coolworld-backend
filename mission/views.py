from django.shortcuts import render
import datetime
from django.http import HttpResponse, JsonResponse, Http404
from .models import Mission
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
import json, base64
from django.core.files.base import ContentFile
import unicodedata

@csrf_exempt
def create(request):
    try:
        if (request.method == 'POST'):
            data = json.loads(request.body)
            survey_answers = data.get('survey_answers')

            if not survey_answers:
                return JsonResponse({"error": "No survey answers provided"}, status=400)

            # survey_answers의 원소를 각 변수에 저장 (traffic, diet, recycle ...)
            # 설문 내용 확정 후 수정 예정
            ans1 = survey_answers[0] if len(survey_answers) > 0 else None
            ans2 = survey_answers[1] if len(survey_answers) > 1 else None
            print(ans1, ans2)


            mission = Mission()
            
            # ----- AI 미션 생성 ----- #
            # 임시 코드
            mission_content = "종이컵 대신 텀블러를 사용해보세요."
            mission_category = "일회용품"
            # ----- AI 미션 생성 ----- #

            mission.content = mission_content
            mission.date = timezone.now().date()
            mission.is_successful = False
            mission.image = None
            mission.category = mission_category

            mission.save()

            data = {
                'id': mission.pk,
                'content': mission.content,
                'date': mission.date,
                'category': mission.category,
            }
            return JsonResponse(data=data, safe=False, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def verify(request):
    try:
        if request.method == 'POST':
            mission_date = request.POST['date']
            proof_image = request.FILES['image']
            if not mission_date or not proof_image:
                return JsonResponse({"error": "Date and image are required"}, status=400)

            proof_image = json.dumps(str(proof_image))

            # 해당 날짜의 미션을 조회
            try:
                mission = Mission.objects.get(date=mission_date)
            except Mission.DoesNotExist:
                return JsonResponse({"error": "Mission not found for the given date"}, status=404)
            

            # ---- AI를 호출해 이미지 인증 여부 결정 ---- #
            # is_successful = ai_verify_mission(proof_image)
            # 임시
            import random
            is_successful = random.choice([True, False])
            # ---- AI를 호출해 이미지 인증 여부 결정 ---- #

            # 미션 업데이트
            mission.image = proof_image
            mission.is_successful = is_successful
            mission.save()

            # 응답 데이터 생성
            response_data = {
                "id": mission.pk,
                "content": mission.content,
                "date": mission.date,
                "category": mission.category,
                "is_successful": mission.is_successful,
                "image" : request.build_absolute_uri(mission.image.url),
            }

            return JsonResponse(data=response_data, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def stamp(request):
    try:
        if request.method == 'GET':
            data = json.loads(request.body)
            year = int(data.get('year'))
            month = int(data.get('month'))      

            if not year or not month:
                return JsonResponse({"error": "Year and month are required"}, status=400)

        # 요청받은 연도와 월에 해당하는 미션을 조회
        missions = Mission.objects.filter(date__year=year, date__month=month).order_by('date')

        mission_list = []
        for mission in missions:
            mission_list.append({
                "date": mission.date.strftime("%Y-%m-%d"),
                "status": "success" if mission.is_successful else "fail"
            })

        response_data = {
            "year": year,
            "month": month,
            "missions": mission_list
        }

        return JsonResponse(data=response_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)    