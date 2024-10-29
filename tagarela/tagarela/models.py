#!/usr/bin/env python
# coding: utf-8

from sqlalchemy_utils import ArrowType

from cuidando_utils import db


class Vote(db.Model):
    '''Association table for votes.'''
    __tablename__ = 'votes'
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'),
                           primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'),
                          primary_key=True)
    like = db.Column(db.Boolean(), nullable=False)
    author = db.relationship("Author", backref="votes")
    comment = db.relationship("Comment",
                              backref=db.backref("votes",
                                                 single_parent=True,
                                                 cascade="all, delete-orphan"))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    # created = db.Column(db.DateTime(timezone=True), nullable=False)
    # modified = db.Column(db.DateTime(timezone=True), nullable=False)
    created = db.Column(ArrowType, nullable=False)
    modified = db.Column(ArrowType, nullable=False)
    # http://docs.sqlalchemy.org/en/rel_1_0/orm/basic_relationships.html
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'),
                          nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'),
                          nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'),
                          nullable=True)
    children = db.relationship('Comment',
                               backref=db.backref('parent',
                                                  remote_side=[id]))
    hidden = db.Column(db.Boolean(), default=False)

    def set_vote(self, author_id, like):
        vote = db.session.query(Vote).filter_by(
            comment_id=self.id,
            author_id=author_id
        ).first()

        if vote:
            if vote.like == like:
                # Vote exists and is the same
                return True
            else:
                # Vote exists but changed
                vote.like = like
                if like:
                    # changed to a like
                    self.likes += 1
                    self.dislikes -= 1
                else:
                    # changed to a dislike
                    self.likes -= 1
                    self.dislikes += 1
        else:
            # New vote
            vote = Vote(comment_id=self.id, author_id=author_id, like=like)
            db.session.add(vote)
            if like:
                self.likes += 1
            else:
                self.dislikes += 1
        db.session.commit()


class Thread(db.Model):
    __tablename__ = 'thread'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    comments = db.relationship("Comment", backref="thread")


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    comments = db.relationship("Comment", backref="author")
