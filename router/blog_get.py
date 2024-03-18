from fastapi import APIRouter, status, Response, Depends
from enum import Enum
from typing import Optional
from router.blog_post import required_functionality


router = APIRouter(
    prefix='/blog',
    tags=['blog']#tags used for categorizing endpoints
)


@router.get('/all',
         summary='Retrieve all blogs',
         description='This api call simulates fetching all blogs',
         response_description='list of available blogs'
        )
def get_blogs(page = 1, page_size: Optional[int] = None,
              req_parameter: dict = Depends(required_functionality)): #defining parameters and assigning an optional parameters
    return {'message':
            f'All {page_size} blogs on page {page}', 'req': req_parameter}

@router.get('/{id}/comments/{comment_id}', tags=['comment'])
def get_comment(id: int, comment_id: int,
                valid: bool = True, username: Optional[str]= None,
                req_parameter: dict = Depends(required_functionality)):
    """
    Simulate retreiving a comment of a blog

    - **id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** optional query parameter
    - **username** optional query parameter
    """
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}, required_functionality {req_parameter}'}

#To display the /blog/all path endpoint in the browser
#it must be in the above the /blog
#@app.get('/blog/all')
#def get_all_blogs():
#    return {'message': 'All blogs provided'}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('/type/{temp}')
def get_blog_type(temp: BlogType,
                req_parameter: dict = Depends(required_functionality)):
    return {'message': f'Blog type of {temp.value} and req functionality {req_parameter}'}

@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response,
            req_parameter: dict = Depends(required_functionality)):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Blog {id} not found, req func {req_parameter}'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'message': f'Blog with id {id}, req func {req_parameter}'}