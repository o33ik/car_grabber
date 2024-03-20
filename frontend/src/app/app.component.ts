import { Component } from '@angular/core';
import {FormControl, FormGroup} from "@angular/forms";
import {DataService} from "./shared/services/data.service";
import {AutoRiaCar} from "./shared/models/auto-ria-car";
import {CarDetailsDialogComponent} from "./components/car-details-dialog/car-details-dialog.component";
import {MatDialog} from "@angular/material/dialog";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'car-grabber-frontend';

  formGroup: FormGroup = new FormGroup<any>({
    url: new FormControl('https://auto.ria.com/uk/search/?categories.main.id=1&brand.id[0]=24&model.id[0]=241&indexName=auto,order_auto,newauto_search&engine.gte=2.4&engine.lte=2.6&price.USD.lte=10000')
  });


  constructor(private dataService: DataService,
              private dialog: MatDialog,) {
    setTimeout(() => {
      this.submit()
    }, 100)
  }

  cars: AutoRiaCar[] = [];

  submit() {
    this.dataService.getAutoRiaList(this.formGroup.value.url).subscribe((cars) => {
      this.cars = cars;
    })
  }

  searchByVin(vin: string) {
    const dialogRef = this.dialog.open(CarDetailsDialogComponent, {
      data: {
        vin,
      },
    });
  }
}
