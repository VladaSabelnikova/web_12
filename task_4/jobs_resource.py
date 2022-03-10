from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.jobs import Jobs
from parsers import parser_editing_job, parser_add_job


class BaseJobsResourceClass(Resource):

    def abort_if_jobs_not_found(self, job_id):
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        if not job:
            abort(404, message=f'Job {job_id} not found')


class JobsResource(BaseJobsResourceClass):

    def get(self, job_id):
        self.abort_if_jobs_not_found(job_id)

        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        all_attributes = (
            'id',
            'job',
            'work_size',
            'collaborators',
            'start_date',
            'end_date',
            'is_finished',
            'user.name',
            'user.surname',
        )

        return jsonify({'job': job.to_dict(only=all_attributes)})

    def delete(self, job_id):
        self.abort_if_jobs_not_found(job_id)
        db_sess = db_session.create_session()
        user = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'info': ' successfully'})

    def post(self, job_id):
        self.abort_if_jobs_not_found(job_id)
        args = parser_editing_job.parse_args()
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()

        job.job = args.get('job', job.job)
        job.work_size = args.get('work_size', job.work_size)
        job.collaborators = args.get('collaborators', job.collaborators)
        job.is_finished = args.get('is_finished', job.is_finished)
        job.team_leader = args.get('team_leader', job.team_leader)

        db_sess.add(job)
        db_sess.commit()

        return jsonify({'info': ' successfully'})


class JobsListResource(Resource):
    def get(self):
        all_attributes = (
            'id',
            'job',
            'work_size',
            'collaborators',
            'start_date',
            'end_date',
            'is_finished',
            'user.name',
            'user.surname',
        )
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return jsonify(
            {'jobs': [item.to_dict(only=all_attributes) for item in jobs]}
        )

    def post(self):
        args = parser_add_job.parse_args()
        db_sess = db_session.create_session()

        job = Jobs()
        job.job = args['job']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        job.team_leader = args['team_leader']

        db_sess.add(job)
        db_sess.commit()

        return jsonify({'info': ' successfully'})
