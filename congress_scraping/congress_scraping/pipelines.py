# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, SenateMember


engine = create_engine('sqlite:///database.db')


class StoragePipeline:

    def __init__(self, db_engine=engine):
        self.engine = db_engine
        Base.metadata.create_all(self.engine)

    def open_spider(self, spider):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        member = (
            self.session.query(SenateMember).filter_by(name=item['name']).first()
        )
        
        if member is None:
            member = SenateMember(name=item['name'])
        
        member.img_url = item['picture']
        member.party = item['party']
        member.birth_date = item['birth_date']
        member.city = item['city']
        member.com_const = item['com_const']
        member.twitter = item['twitter']

        self.session.add(member)
        self.session.commit()

