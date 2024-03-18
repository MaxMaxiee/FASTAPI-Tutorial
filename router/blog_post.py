from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metatdata: Dict[str, str] = {"key1": "val1"}
    image: Optional[Image] = None

@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        'id': id,
        'data': blog,
        'version': version,
        }
    #return {'blog_title': blog.title,
    #        'blog_content': blog.content,
    #        'blog_nb_comments': blog.nb_comments,
    #        'blog_published': blog.published}

@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel, id: int,
                    comment_title: int = Query(None,
                        title='Title of the comment',
                        description='Some description for comment_title',
                        alias='commentTitle',
                        deprecated=True),
                    #content: str = Body('hi how are you') #optional value/can be deleted
                    #content: str = Body(Ellipsis) #Similar way of not optional value
                    #Not an optional value. Value is required
                    content: str = Body(...,
                        min_length=10,
                        max_length=12,
                        regex='^[a-z\\s]*$'),#Value must be lower case
                    v: List[Optional[str]] = Query(['1.0', '1.1', '1.2']),
                    comment_id: int = Path(gt=5, le=10)
    ):
    return {
        'body': blog,
        'id': id,
        'comment_title': comment_title,
        'content': content,
        'version': v,
        'comment_id': comment_id
    }

def required_functionality():
    return {'message': 'Learning FastAPI is important'}