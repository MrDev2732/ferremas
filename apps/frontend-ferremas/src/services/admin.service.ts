import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../app/interfaces/user';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = 'http://localhost:8000/get-users';
  private apiUrlDelete = 'http://localhost:8000/delete-user';
  private apiUrlCreate = 'http://localhost:8000/create-user';
  private apiUrlUpdate = 'http://localhost:8000/update-user';

  constructor(private http: HttpClient) { }

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl);
  }

  deleteUser(userId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrlDelete}?user_id=${userId}`);
  }

  createUser(user: User): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.apiUrlCreate}?name=${user.name}&password=${user.password}&rol=${user.rol}`, {});
  }

  updateUser(userId: number, user: User): Observable<{ detail: string }> {
    const url = `${this.apiUrlUpdate}?user_id=${userId}&name=${user.name}&password=${user.password}&rol=${user.rol}`;
    return this.http.put<{ detail: string }>(url, {});
  }

}
