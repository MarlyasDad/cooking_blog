from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from . import Base


tags_association_table = Table(
    'cblog_tagsassociation',
    Base.metadata,
    Column('receipt_id', Integer, ForeignKey('cblog_receipt.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('cblog_tag.id'), primary_key=True)
)


# class TagsAssociation(Base):
#     receipt_id = Column(Integer, ForeignKey('cblog_receipt.id'))
#     tag_id = Column(Integer, ForeignKey('cblog_tag.id'))
#
#     tag = relationship("Tag", back_populates="receipts")
#     receipt = relationship("Receipt", back_populates="tags")


class Tag(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    receipts = relationship('Receipt', secondary=tags_association_table,
                            back_populates='tags')

    # receipts = relationship('TagsAssociation', back_populates='tag')

    def __repr__(self):
        return f'<Tag #{self.id} {self.name}>'
