/*
 *
 * Copyright (c) 2017 Red Hat, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

package io.radanalytics.als

import java.util

import org.apache.spark.api.java.JavaRDD
import org.apache.spark.mllib.recommendation.MatrixFactorizationModel

import scala.collection.JavaConverters._

object ALSSerializer {

  private def unpack(factor: Array[Any]): (Int, Array[Double]) = {
    (factor(0).asInstanceOf[Int],
      factor(1).asInstanceOf[util.ArrayList[Double]].asScala.toArray)
  }

  def instantiateModel(rank: Int,
                      userFactors: JavaRDD[Array[Any]],
                      productFactors: JavaRDD[Array[Any]]): MatrixFactorizationModel = {

    val userRDD = userFactors.rdd.map(unpack)

    val productRDD = productFactors.rdd.map(unpack)

    new MatrixFactorizationModel(rank = rank,
      userFeatures = userRDD,
      productFeatures = productRDD)

  }

}