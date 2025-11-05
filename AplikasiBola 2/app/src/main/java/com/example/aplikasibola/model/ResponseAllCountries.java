package com.example.aplikasibola.model;

import java.util.List;
import com.google.gson.annotations.SerializedName;

public class ResponseAllCountries{

	@SerializedName("countries")
	private List<CountriesItem> countries;

	public void setCountries(List<CountriesItem> countries){
		this.countries = countries;
	}

	public List<CountriesItem> getCountries(){
		return countries;
	}

	@Override
 	public String toString(){
		return 
			"ResponseAllCountries{" + 
			"countries = '" + countries + '\'' + 
			"}";
		}
}