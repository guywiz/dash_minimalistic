from view.histogramFactory import HistogramFactory
from view.layoutManager import LayoutManager

class ViewManager:
	def __init__(self, data_manager):
		self.data_manager = data_manager
		self.layout_manager = LayoutManager()
		self.histogram_maker = HistogramFactory()

	def get_layout(self, data_manager):
		return self.layout_manager.get_layout(data_manager)
	
	def update_histograms(self, selected_values):
		figs = []

		for i, f in enumerate(self.data_manager.get_feature_names()):
			val = selected_values[f]
			figs.append(self.histogram_maker.make_histogram(f, val, self.data_manager))

		return figs
	
	def update_selected_values(self, *args):

		*clicks, current = args

		new_vals = current.copy()

		for i, click in enumerate(clicks):
			if click:
				x = click["points"][0]["x"]
				new_vals[self.data_manager.get_feature_names()[i]] = float(x)

		return new_vals

	def update_prediction(self, selected_values):
		x = [selected_values[f] for f in self.data_manager.get_feature_names()]

		pred = self.data_manager.get_model_prediction(x)
		proba = self.data_manager.get_model_proba(x)

		pred_name = self.data_manager.get_target_names()[pred]
		
		proba_list = self.layout_manager.get_Ul_list(proba, self.data_manager.get_target_names())
		#proba_list = html.Ul([
		#    html.Li(f"{self.data_manager.get_target_names()[i]} : {proba[i]:.3f}")
		#    for i in range(len(self.data_manager.get_target_names()))
		#])

		return f"Classe prédite : {pred_name}", proba_list
