from datetime import datetime
from typing import List, Tuple
from ..models.group_request import GroupRequest, RequestStatus, RequestType


def __tuple_to_request(row: Tuple[int, int, int, datetime, int, int, datetime]) -> GroupRequest:
    id, group_id, student_id, created, status, request_type, last_update = row
    return GroupRequest(
        id=id,
        group_id=group_id,
        student_id=student_id,
        created=created,
        status=status,
        type=request_type,
        last_update=last_update
    )


def get_student_requests(conn, student_id: int) -> List[GroupRequest]:
    """
    Retrieves existing group requests from student with given id
    @param conn - Database connection
    @param student_id - searched student id
    @return list of all group requests
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, group_id, student_id, created, status, type, last_update '
                   'FROM group_request WHERE student_id = %s', (student_id,))
    rows = cursor.fetchall()
    return list(map(__tuple_to_request, rows))


def create_request(conn, student_id: int, group_id: int, type: RequestType):
    """
    Creates new group request for given student and group id
    @param conn - Database connection
    @param student_id - given student id
    @param group_id - given group id
    @param type - request type for new request
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO group_request (student_id, group_id, type, status, last_update, created) '
                   'VALUES (%s, %s, %s, 0, now(), now())', (student_id, group_id, type.value))
    conn.commit()


def update_request_status(conn, request_id: int, status: RequestStatus):
    """
    Creates new group request for given student and group id
    @param conn - Database connection
    @param request_id - given request id
    @param status - new status
    """
    cursor = conn.cursor()
    cursor.execute('UPDATE group_request SET last_update = now(), status = %s WHERE id = %s', (status.value, request_id))
    conn.commit()
