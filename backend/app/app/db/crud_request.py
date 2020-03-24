from typing import List, Tuple
from ..models.group_request import GroupRequest


def __tuple_to_request(row: Tuple[int, int, int, str, int, str]) -> GroupRequest:
    id, group_id, student_id, created_timestamp, status, last_updated = row
    return GroupRequest(
        id=id,
        group_id=group_id,
        student_id=student_id,
        created_timestamp=created_timestamp,
        status=status,
        last_updated=last_updated
    )


def get_student_requests(conn, student_id: int) -> List[GroupRequest]:
    """
    Retrieves existing group requests from student with given id
    @param conn - Database connection
    @param student_id - searched student id
    @return list of all group requests
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, group_id, student_id, created_timestamp, status, last_updated'
                   'FROM group_request WHERE student_id = %s', (student_id,))
    rows = cursor.fetchall()
    return list(map(__tuple_to_request, rows))


def create_request(conn, student_id: int, group_id: int):
    """
    Creates new group request for given student and group id
    @param conn - Database connection
    @param student_id - given student id
    @param group_id - given group id
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO group_request (student_id, group_id) VALUES (%s, %s)', (student_id, group_id))
    conn.commit()


def update_request_status(conn, request_id: int, status: int):
    """
    Creates new group request for given student and group id
    @param conn - Database connection
    @param request_id - given request id
    @param status - new status
    """
    cursor = conn.cursor()
    cursor.execute('UPDATE group_request SET last_updated = now(), status = %s WHERE id = %s', (status, request_id))
    conn.commit()
