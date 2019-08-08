from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from question.models import Option, Question


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Option
        fields = ('id', 'option', 'correct')


class QuestionReadSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'body', 'options')


class QuestionWriteSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'body', 'options')

    def create(self, validated_data):
        options = validated_data.pop('options')
        question = Question.objects.update_or_create(**validated_data)

        option_query = Option.objects.filter(question=question[0])
        if len(option_query) > 1:
            for existing_option in option_query:
                option_query.delete()

        for option in options:
            Option.objects.create(question=question[0], **option)

        return question[0]

    def validate(self, attrs):
        all_options = []
        all_correct_options = []

        for option in attrs['options']:
            all_options.append(option['option'].lower())
            all_correct_options.append(option['correct'])

        for option in all_options:
            if all_options.count(option) > 1:
                raise serializers.ValidationError({"options": _("Options must be unique")})
            elif all_correct_options.count(1) > 1:
                raise serializers.ValidationError({"options": _("Only one option can be true for a question")})
            elif all_correct_options.count(1) < 1:
                raise serializers.ValidationError({"options": _("At least one option need to be correct")})
            else:
                pass
        return attrs


class QuestionUpdateSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'body', 'options')

    def update(self, instance, validated_data):
        options = validated_data.pop('options')
        instance.body = validated_data.get('body', instance.body)
        instance.save()

        keep_options = []
        for option_data in options:
            if 'id' in option_data.keys():
                if Option.objects.filter(id=option_data['id'], question_id=instance.id).exists():
                    option = Option.objects.get(id=option_data['id'])
                    option.option = option_data.get('option', option.option)
                    option.correct = option_data.get('correct', option.correct)
                    option.save()
                    keep_options.append(option.id)
                else:
                    continue
            else:
                option = Option.objects.create(**option_data, question=instance)
                keep_options.append(option.id)
        for option in instance.options.all():
            if option.id not in keep_options:
                Option.objects.filter(id=option.id).delete()

        return instance

    def validate(self, attrs):
        all_options = []
        all_correct_options = []

        for option in attrs['options']:
            all_options.append(option['option'].lower())
            all_correct_options.append(option['correct'])

        for option in all_options:
            if all_options.count(option) > 1:
                raise serializers.ValidationError({"options": _("Options must be unique")})
            elif all_correct_options.count(1) > 1:
                raise serializers.ValidationError({"options": _("Only one option can be true for a question")})
            elif all_correct_options.count(1) < 1:
                raise serializers.ValidationError({"options": _("At least one option need to be correct")})
            else:
                pass
        return attrs
