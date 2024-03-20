import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {AutoRiaCar} from "../models/auto-ria-car";

@Injectable({
  providedIn: 'root',
})
export class DataService {

  private apiUrl = 'http://127.0.0.1:5000'

  constructor(private http: HttpClient) { }

  getAutoRiaList(url: string): Observable<AutoRiaCar[]> {
    return this.http.post<{ cars: AutoRiaCar[] }>(`${this.apiUrl}/autoria`, {url}).pipe(
      map(({cars}) => cars)
    );
  }

  getCarsData(vin: string): Observable<{ result: string, imageUrls: string[] }> {
    return this.http.get<{ result: any }>(`${this.apiUrl}//bidfax/${vin}`).pipe(
      map((res) => ({imageUrls: res.result.image_urls, result: res.result.result}))
    );
  }
}
