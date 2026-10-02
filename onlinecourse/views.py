def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    if request.method == 'POST':
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))
        
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_choice_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        submission.save()
        
        return redirect('onlinecourse:exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    questions = Question.objects.filter(courses=course)
    for question in questions:
        selected_choices = submission.choices.filter(question=question)
        selected_ids = [c.id for c in selected_choices]
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    context['course'] = course
    context['grade'] = total_score
    context['submission'] = submission
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)