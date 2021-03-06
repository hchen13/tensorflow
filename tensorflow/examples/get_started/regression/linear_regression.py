# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Linear regression using the LinearRegressor Estimator."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

import imports85  # pylint: disable=g-bad-import-order

STEPS = 1000


def main(argv):
  """Builds, trains, and evaluates the model."""
  assert len(argv) == 1
  (x_train, y_train), (x_test, y_test) = imports85.load_data()

  # Build the training input_fn.
  input_train = tf.estimator.inputs.pandas_input_fn(
      x=x_train,
      y=y_train,
      # Setting `num_epochs` to `None` lets the `inpuf_fn` generate data
      # indefinitely, leaving the call to `Estimator.train` in control.
      num_epochs=None,
      shuffle=True)

  # Build the validation input_fn.
  input_test = tf.estimator.inputs.pandas_input_fn(
      x=x_test, y=y_test, shuffle=True)

  feature_columns = [
      # "curb-weight" and "highway-mpg" are numeric columns.
      tf.feature_column.numeric_column(key="curb-weight"),
      tf.feature_column.numeric_column(key="highway-mpg"),
  ]

  # Build the Estimator.
  model = tf.estimator.LinearRegressor(feature_columns=feature_columns)

  # Train the model.
  # By default, the Estimators log output every 100 steps.
  model.train(input_fn=input_train, steps=STEPS)

  # Evaluate how the model performs on data it has not yet seen.
  eval_result = model.evaluate(input_fn=input_test)

  # The evaluation returns a Python dictionary. The "average_loss" key holds the
  # Mean Squared Error (MSE).
  average_loss = eval_result["average_loss"]

  # Convert MSE to Root Mean Square Error (RMSE).
  print("\n" + 80 * "*")
  print("\nRMS error for the test set: ${:.0f}".format(average_loss**0.5))

  # Run the model in prediction mode.
  input_dict = {
      "curb-weight": np.array([2000, 3000]),
      "highway-mpg": np.array([30, 40])
  }
  predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      input_dict, shuffle=False)
  predict_results = model.predict(input_fn=predict_input_fn)

  # Print the prediction results.
  print("\nPrediction results:")
  for i, prediction in enumerate(predict_results):
    msg = ("Curb weight: {: 4d}lbs, "
           "Highway: {: 0d}mpg, "
           "Prediction: ${: 9.2f}")
    msg = msg.format(input_dict["curb-weight"][i], input_dict["highway-mpg"][i],
                     prediction["predictions"][0])

    print("    " + msg)
  print()


if __name__ == "__main__":
  # The Estimator periodically generates "INFO" logs; make these logs visible.
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run(main=main)
