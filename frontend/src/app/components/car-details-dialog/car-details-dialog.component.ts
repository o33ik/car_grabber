import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA} from "@angular/material/dialog";
import {DataService} from "../../shared/services/data.service";

@Component({
  selector: 'app-car-details-dialog',
  templateUrl: './car-details-dialog.component.html',
  styleUrl: './car-details-dialog.component.scss'
})
export class CarDetailsDialogComponent {
  imageUrls: null | string[] = null;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any,
              private dataService: DataService,
              ) {
    this.dataService.getCarsData(data.vin).subscribe(res => {
      this.imageUrls = res.imageUrls;
    })
  }
}
