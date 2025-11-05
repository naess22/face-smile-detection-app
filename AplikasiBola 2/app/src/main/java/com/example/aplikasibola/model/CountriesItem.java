package com.example.aplikasibola.model;

import java.util.List;
import com.google.gson.annotations.SerializedName;

public class CountriesItem{

	@SerializedName("countries")
	private List<CountriesItem> countries;

	@SerializedName("name_en")
	private String nameEn;

	public void setCountries(List<CountriesItem> countries){
		this.countries = countries;
	}

	public List<CountriesItem> getCountries(){
		return countries;
	}

	public void setNameEn(String nameEn){
		this.nameEn = nameEn;
	}

	public String getNameEn(){
		return nameEn;
	}

	@Override
 	public String toString(){
		return 
			"CountriesItem{" + 
			"countries = '" + countries + '\'' + 
			",name_en = '" + nameEn + '\'' + 
			"}";
		}
}