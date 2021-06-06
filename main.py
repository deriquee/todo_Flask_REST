from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class TaskModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	details = db.Column(db.String(500), nullable=False)
	

	def __repr__(self):
		return f"Task(name = {name}, details = {details})"

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("name", type=str, help="Name of the task is required", required=True)
task_put_args.add_argument("details", type=str, help="Details of the task", required=True)


task_update_args = reqparse.RequestParser()
task_update_args.add_argument("name", type=str, help="Name of the task is required")
task_update_args.add_argument("details", type=str, help="Details of the task")


resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'details': fields.String,
	
}

class Task(Resource):
	@marshal_with(resource_fields)
	def get(self, task_id):
		result = TaskModel.query.filter_by(id=task_id).first()
		if not result:
			abort(404, message="Could not find task with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, task_id):
		args = task_put_args.parse_args()
		result = TaskModel.query.filter_by(id=task_id).first()
		if result:
			abort(409, message="Task id taken...")

		task = TaskModel(id=task_id, name=args['name'], details=args['details'])
		db.session.add(task)
		db.session.commit()
		return task, 201

	@marshal_with(resource_fields)
	def patch(self, task_id):
		args = task_update_args.parse_args()
		result = TaskModel.query.filter_by(id=task_id).first()
		if not result:
			abort(404, message="Task doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['details']:
			result.details = args['details']
		

		db.session.commit()

		return result


	def delete(self, task_id):
		abort_if_task_id_doesnt_exist(task_id)
		del tasks[task_id]
		return '', 204


api.add_resource(Task, "/task/<int:task_id>")

if __name__ == "__main__":
	app.run(debug=True)